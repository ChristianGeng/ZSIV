#from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse
from .models import Journals
from .models import MAJournal
from .models import Mitarbeiter
from .models import Summaries
from .models import Choice, Question
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

# def index(request):
#     journallist = Journals.objects.order_by('Name')
# 
#     #output = ' ,'.join([q.Name for q in journallist])
#     templatename = 'ZSIV/index.html'
#     #template = loader.get_template(templatename)
#     context = {
#         'journallist': journallist,
#     }
#     #return HttpResponse(template.render(context, request))
#     return render(request, templatename, context)
#     #return HttpResponse("Hello, world. You're at the ZSIV  index.")



#class SnippetListAll(ListView):
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse_lazy


from django.forms.models import modelform_factory

"""
Cooler Mixin, der die formfactory zum reinmixen von widgets erlaubt
http://stackoverflow.com/questions/16937076/how-does-one-use-a-custom-widget-with-a-generic-updateview-without-having-to-red
"""
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


def home():
    pass

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
    #fields = ['Filename']

class SummariesDeleteView(DeleteView):
    model = Summaries
    success_url = reverse_lazy('Summaries-list')
    model = Summaries


class SummariesDetailView(DetailView):
    model = Summaries
    #template_name = 'ZSIV/Summaries-Detail.html'
    fields = '__all__'
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




# def summaries_view(request):
#     if request.method == 'POST':
#         form = SummariesForm(request.POST)
#         if form.is_valid():
#             summaries = form.cleaned_data.get('summaries')
# 
#     else:
#         form = SummariesForm
#         
#     context = {'form':form }
#     return render(request, 'ZSIV/render_summaries.html', context)





# def MAjournals_view_formset(request):
#     mitarbeiter_id = 1
#     #majournals = MAJournal MA_id=mitarbeiter_id
#     
#     ma = Mitarbeiter.objects.get(pk=mitarbeiter_id)
#     JournalInlineFormSet = inlineformset_factory(MAJournal,Journals, fields=('Name',))
#     if request.method == "POST":
#         formset = JournalInlineFormSet(request.POST, request.FILES, instance=ma)
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             return HttpResponseRedirect(ma.get_absolute_url())
#     else:
#         formset = JournalInlineFormSet(instance=ma)
#     return render(request, 'render_majournals', {'formset': formset})


    
# def MAjournals_view(request):
#     if request.method == 'POST':
#         form = MAJournalForm(request.POST)
#         if form.is_valid():
#             MAjournals = form.cleaned_data.get('MAjournals')
# 
#     else:
#         form = MAJournalForm
#         
#     context = {'form':form }
#     return render(request, 'ZSIV/render_majournals.html', context)

    
# def JournalIndexView(request):    
#     form = modelform_factory(Journals,form=JournalForm)
#     #context = {'form':form }
#     formTemplate = 'ZSIV/vanillaSave.html'
#     context = {'form':form }
#     return render(request, formTemplate, context)
    

# class JournalList(ListView):
#     queryset = Journals.objects.order_by('Name')
#     context_object_name = 'book_list'
    #print("request method: ; ",request.method)
    
    
class JournalList(ListView):
    model = Journals
    templatename = 'ZSIV/meineListe.html'





def MA_Subscribe_Journals(request, mitarbeiter_id): 
#     #subscr = get_object_or_404(Journals,pk=mitarbeiter_id)
#     #ma  = get_object_or_404(Mitarbeiter, pk=1)
#     formTemplate = 'ZSIV/vanillaSave.html'
#      = Mitarbeiter.objects.filter(pk=mitarbeiter_id).select_related()
     # 
     

    formTemplate = 'ZSIV/vanillaSave.html'
    mitarbeiter_list = Mitarbeiter.objects.filter(pk=mitarbeiter_id).select_related()
    Mitarbeiter.objects.filter(pk=mitarbeiter_id).select_related().values()
    mymitarbeiter = mitarbeiter_list[0]
    
    # linking data
    ma_journal_data = MAJournal.objects.filter(MA_id=mitarbeiter_id) #linking table
    initialvalues = [x['Journal_id'] for x in mymitarbeiter.majournal_set.values()]

    
    
    
    print ('ma_journal_data',ma_journal_data)
    print ("mitarbeiter_id", mitarbeiter_id)
    print ("mymitarbeiter", mymitarbeiter)
    
    print("request method: ; ",request.method)
    print ("Form Template used; ", formTemplate) 
    if request.method == 'POST':
        form = MitarbeiterForm(request.POST, initial={'Subscriptions': initialvalues}, instance=mymitarbeiter)
        print(form.data)
        print (form.Meta)
        
        if form.is_valid():
            print ("Is form valid?" , form.is_valid())
            
            #journals = form.cleaned_data.get('journals')
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
    print ('ma_journal_data',ma_journal_data)
    print ("journal _id", journal_id)
    print("request method: ; ",request.method)
    print ("Form Template used; ", formTemplate) 
    if request.method == 'POST':
        #form = JournalForm(request.POST)
        form = JournalForm(request.POST, initial={'Subscriptions': initialvalues}, instance=myjournal)
        #print (form.data)
        #print (form.cleaned_data)
        if form.is_valid():
            print ("Is form valid?" , form.is_valid())
            
            #journals = form.cleaned_data.get('journals')
            MA_ids_subscribe = form.data.getlist('Subscriptions') # ids
            print ('Substr:' , MA_ids_subscribe)
            ma_journal_data.delete()
            for x in MA_ids_subscribe: ma_journal_data.update_or_create(Journal_id=journal_id, MA_id = x)
            
            context = {'form':form}
            #return render(request, formTemplate, context)
        return HttpResponseRedirect(reverse('ZSIV:indexJournal'))
    else:
        form = JournalForm(initial={'Subscriptions': initialvalues}, instance=myjournal)
        context = {'form':form}
        return render(request, formTemplate, context)
        #form = JournalForm











# from polls app
class IndexView(generic.ListView):
    template_name = 'ZSIV/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

#class DetailView(generic.DetailView):
#    model = Question
#    template_name = 'ZSIV/detail.html'
    # for Part 5: Testing the DetailView:
    # wir brauchen eine weitere Methode get_queryset
    # die uns die aus der Zukunft nicht gibt
#    def get_queryset(self):
#        """
#        Excludes any questions that aren't published yet.
#        """
#        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ZSIV/results.html'



