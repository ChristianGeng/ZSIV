from django.http import HttpResponse
from .models import Journals
from .models import MAJournal
from .models import Mitarbeiter
from .models import Summaries
#from .models import Choice, Question
from django.template import RequestContext
#from django.template import loader
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.utils import timezone
from django.template.context_processors import request
from .forms import JournalForm
from ZSIV.forms import SummariesForm, MAJournalForm, MitarbeiterForm
from django.forms import inlineformset_factory
from django.forms.models import modelformset_factory
from django.forms import modelformset_factory, modelform_factory
from django.forms.formsets import formset_factory
from django.views.generic import ListView, DetailView
from django.forms.widgets import CheckboxInput, SelectMultiple, Select
from pandas.tseries.frequencies import _name
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
















"""
GoDjango: 

The Class Based "View" (https://godjango.com/69-the-class-based-view/)
- Wann imemr asview benuttz wird, wird die dispatch Methode des Class based views aufgerufen
- inspiziert was die request methode ist

Class Based Views Part 1: TemplateView and RedirectView 
(https://godjango.com/15-class-based-views-part-1-templateview-and-redirectview/)
Template View
- Use of get_context_data(self, kwargs)
get data from databse and send to template; Normally trough context, 
now override get_context_data. Die Methode wird aus der superclasse initialisiert
- template_name - wie immer 
- as_view() method
- Redirect view: 
es wird die get-Methode implementiert. 
Warum: by default: all directs are permanent, dieses mal will man das nicht
Und wir brauchen einen url, auf den geredirected werden kann

Class Based Views Part 2: ListView and FormView

ListView
- Was tut: der SummariesCreateView (name='Summaries-add')
- redirected auf den  Summaries-all view
Dieser weiss das aufgrund der get_absolute_url(self) methode im modell Summaries
- dies ist ein ListView, welcher in urls.py direkt implementiert ist- 

FormView:
- Displays a form
- on error redisplays form with validation errors
- on success redirects to new url
* form_class = Taskform
* success_url


Class Based Views Part 3: DetailView and template_name Shortcut

template name shortcut: 
app/model_detail.html -> ZSIV/templates/Summaries_detail.html
app/model_list.html    -> ZSIV/templates/Summaries_List.html


Understanding get_absolute_url
https://godjango.com/67-understanding-get_absolute_url/


"""




"""
Cooler Mixin, der die formfactory zum reinmixen von widgets erlaubt
http://stackoverflow.com/questions/16937076/how-does-one-use-a-custom-widget-with-a-generic-updateview-without-having-to-red
"""
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


"""
class based view and file uploads:
http://www.kelvinwong.ca/2013/09/19/upload-files-using-filefield-and-generic-class-based-views-in-django-1-5/
https://godjango.com/35-upload-files/
"""
class SummariesCreateView(ModelFormWidgetMixin,CreateView):
#class SummariesCreateView(CreateView):
    model = Summaries
    #fields = ['Filename']
    fields = '__all__'
    #template_name = 'ZSIV/filehandling.html'
    template_name = 'ZSIV/Summaries-create.html'
    widgets = {
        #'PublicationDate': SelectDateWidget,
        'SENT' : CheckboxInput,
#        'Heftnummer' :  Select,
        'Heftnummer' :  Select,
    }
    
class SummariesUpdateView(UpdateView):
    model = Summaries
    fields = '__all__'
    template_name = 'ZSIV/summaries_form.html' #  is the default
    widgets = {
        #'PublicationDate': SelectDateWidget,
        'SENT' : CheckboxInput,
#        'Heftnummer' :  Select,
        'Heftnummer' :  Select,
    }
    context_object_name = 'summary'
    
    #fields = ['Filename']

class SummariesDeleteView(DeleteView):
    model = Summaries
    success_url = reverse_lazy('Summaries-list')
    model = Summaries


class SummariesDetailView(DetailView):
    model = Summaries
    template_name = 'ZSIV/summaries_detail.html'
    #template_name = 'ZSIV/Summaries-Detail.html'
    fields = '__all__'
    #widgets = {
    #    #'PublicationDate': SelectDateWidget,
    #    'SENT' : CheckboxInput,
#        'Heftnummer' :  Select,
    #    'Heftnummer' :  Select,
    #}

    #def get_object(self):
    #    return get_object_or_404(Summaries, pk=id)
    #template_name = 'ZSIV/filehandling.html'


class indexViewJournals(generic.ListView):
    template_name='ZSIV/indexJournal.html'
    context_object_name = 'list_to_view'
    def get_queryset(self):
        return Journals.objects.filter().order_by('Name')


class indexViewMA(generic.ListView):
    template_name = 'ZSIV/indexMA.html'
    context_object_name = 'list_to_view'
    def get_queryset(self):
        return Mitarbeiter.objects.filter().order_by('Nachname')

class DetailViewMA(generic.DetailView):
    model = Mitarbeiter
    template_name = 'ZSIV/detailMA.html'
    
class JournalList(ListView):
    model = Journals
    templatename = 'ZSIV/meineListe.html'


def MA_Subscribe_Journals(request, mitarbeiter_id): 

    formTemplate = 'ZSIV/vanillaSave.html'
    mitarbeiter_list = Mitarbeiter.objects.filter(pk=mitarbeiter_id).select_related()
    Mitarbeiter.objects.filter(pk=mitarbeiter_id).select_related().values()
    mymitarbeiter = mitarbeiter_list[0]
    
    # linking data
    ma_journal_data = MAJournal.objects.filter(MA_id=mitarbeiter_id) #linking table
    initialvalues = [x['Journal_id'] for x in mymitarbeiter.majournal_set.values()]
    if request.method == 'POST':
        form = MitarbeiterForm(request.POST, initial={'Subscriptions': initialvalues}, instance=mymitarbeiter)
        print(form.data)
        print (form.Meta)
        
        if form.is_valid():
            print ("Is form valid?" , form.is_valid())
            Journal_ids_subscribe = form.data.getlist('Subscriptions') # ids
            print ('Substr:' , Journal_ids_subscribe)
            ma_journal_data.delete()
            for x in Journal_ids_subscribe: ma_journal_data.update_or_create(  MA_id= mitarbeiter_id, Journal_id = x)
            context = {'form':form}
            #return render(request, formTemplate, context)
        return HttpResponseRedirect(reverse('ZSIV:indexMA'))
    else:
        form = MitarbeiterForm( initial={'Subscriptions': initialvalues}, instance=mymitarbeiter)
        context = {'form':form}
        #return render(request, formTemplate, context)
        return render(request, formTemplate, context)
        
        
           #orig  for x in MA_ids_subscribe: ma_journal_data.update_or_create(Journal_id=journal_id, MA_id = x)
            
def Journal_Subscribe_MAs(request,journal_id):
    """
    indexJournal THIS ONE IS FUNCTIONAL!! # Todo - temp kommentar
    Subscribieren von 
    url(r'^JournalSubscribe/(?P<journal_id>[0-9]+)/$', views.Journal_Subscribe_MAs, name='JournalSubscribe'), #http://localhost:8000/ZSIV/JournalSubscribe/
    
    """
    
    formTemplate = 'ZSIV/vanillaSave.html'
    #journal_id=1
    #myjournal  = get_object_or_404(Journals, pk=journal_id).select_related()

    journallist = Journals.objects.filter(pk=journal_id).select_related()
    myjournal = journallist[0] # TODO: pk lookup always first instance
    
    # linking table
    ma_journal_data = MAJournal.objects.filter(Journal_id=journal_id)
    initialvalues = [x['MA_id'] for x in myjournal.majournal_set.values()]
    #print ("initialvalues: ", initialvalues)
    #print ('ma_journal_data',ma_journal_data)
    #print ("journal _id", journal_id)
    #print("request method: ; ",request.method)
    #print ("Form Template used; ", formTemplate) 
    if request.method == 'POST':
        #form = JournalForm(request.POST)
        form = JournalForm(request.POST, initial={'Subscriptions': initialvalues}, instance=myjournal)
        #print (form.data)
        #print (form.cleaned_data)
        if form.is_valid():
            print ("Is form valid?" , form.is_valid())
            
            #journals = form.cleaned_data.get('journals')
            MA_ids_subscribe = form.data.getlist('Subscriptions') # ids
            print ("subscriptions ",MA_ids_subscribe )
            print ("Anzahl subscriptions ",len(MA_ids_subscribe) )
            print ('Substr:' , MA_ids_subscribe)
            ma_journal_data.delete()
            for x in MA_ids_subscribe: ma_journal_data.update_or_create(Journal_id=journal_id, MA_id = x)
            
            context = {'form':form}
            #return render(request, formTemplate, context)
        return HttpResponseRedirect(reverse('ZSIV:indexJournal'))
    else:
        print ("Form nicht gueltig da alles leer?")
        form = JournalForm(initial={'Subscriptions': initialvalues}, instance=myjournal)
        context = {'form':form}
        return render(request, formTemplate, context)
        #form = JournalForm
