from .models import Journals
from .models import MAJournal
from .models import Mitarbeiter
from .models import Summaries
#from .forms import SummariesDeleteFormSet, 
from .forms import SummariesDeleteForm
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
from django.forms.widgets import CheckboxInput, SelectMultiple, Select,\
    TextInput, Textarea
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormView
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.core import mail
from extra_views import FormSetView, ModelFormSetView
from django.conf import settings
from django.forms import fields
from extra_views import SearchableListMixin
from extra_views import SortableListMixin
from django.forms.widgets import HiddenInput
from django.views.generic.base import  TemplateResponseMixin, View
from django.shortcuts import redirect
from django.core import mail
import os

"""

Vies for ZSIV-App:

    # (1) Main Page
    # (2) Manage Subscriptions
    # (3) Manage Summaries
    # (4) Queue and send
    # (5) Versuche 



Notes: 
Notes on Class-Based Views (notes after watching GoDjango-CBV-Videos)

The Class Based "View" (https://godjango.com/69-the-class-based-view/)
- Wann imemr asview benutzt wird, wird die dispatch Methode des Class based views aufgerufen
- inspiziert was die request methode ist


Class Based Views Part 1: TemplateView and RedirectView 

(https://godjango.com/15-class-based-views-part-1-templateview-and-redirectview/)
Template View
- Use of get_context_data(self, kwargs)
get data from database and send to template; Normally trough context, 
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

Understanding get_absolute_url
https://godjango.com/67-understanding-get_absolute_url/

"""



""" (1) Main Page """
def index(request):
    return render_to_response('ZSIV/index.html')



"""
(2) Manage Subscriptions / jeweils ein Listview und ein View, der die Subscriptions managt
(a) Mitarbeiter 
"""
class indexViewMA(generic.ListView):
    """
    List View der Mitarbeiter - um deren Journal Subscriptions zu handeln 
    """
    #template_name = 'ZSIV/indexMA.html' # renamed to default named mitarbeiter_list.html
    context_object_name = 'list_to_view'
    def get_queryset(self):
        return Mitarbeiter.objects.filter().order_by('Nachname')

def MA_Subscribe_Journals(request, mitarbeiter_id): 
    """
    Die Journals eines einzelnen Mitarbeiters - aus  der Liste aller Journals
    """
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

"""
(2) Manage Subscriptions / jeweils ein Listview und ein View, der die Subscriptions managt
(b) Journals
"""            
class indexViewJournals(generic.ListView):
    """
    List View der Journals - um deren MA Subscriptions zu handeln 
    """
    #template_name='ZSIV/indexJournal.html'
    context_object_name = 'list_to_view'
    def get_queryset(self):
        return Journals.objects.filter().order_by('Name')
    
    
def Journal_Subscribe_MAs(request,journal_id):
    """
    Die Mitarbeiter, die ein bestimmtes Journal subscribieren wollen
    """
    
    formTemplate = 'ZSIV/vanillaSave.html'
    journallist = Journals.objects.filter(pk=journal_id).select_related()
    myjournal = journallist[0] # TODO: pk lookup always first instance
    
    # linking table
    ma_journal_data = MAJournal.objects.filter(Journal_id=journal_id)
    initialvalues = [x['MA_id'] for x in myjournal.majournal_set.values()]
    if request.method == 'POST':
        form = JournalForm(request.POST, initial={'Subscriptions': initialvalues}, instance=myjournal)
        if form.is_valid():
            print ("Is form valid?" , form.is_valid())
            #journals = form.cleaned_data.get('journals')
            MA_ids_subscribe = form.data.getlist('Subscriptions') # ids
            print ("subscriptions ",MA_ids_subscribe )
            print ("Anzahl subscriptions ",len(MA_ids_subscribe) )
            print ('Substr:' , MA_ids_subscribe)
            ma_journal_data.delete()
            for x in MA_ids_subscribe: 
                ma_journal_data.update_or_create(Journal_id=journal_id, MA_id = x)
            
            context = {'form':form}
        return HttpResponseRedirect(reverse('ZSIV:indexJournal'))
    else:
        print ("Form nicht gueltig da alles leer?")
        form = JournalForm(initial={'Subscriptions': initialvalues}, instance=myjournal)
        context = {'form':form}
        return render(request, formTemplate, context)




"""
(3) Manage Summaries
(3a) add, update, delete(nicht implementiert!)) + ein MultiDelete
"""

class ModelFormWidgetMixin(object):
    """
    Cooler Mixin, der die formfactory zum reinmixen von widgets erlaubt
    http://stackoverflow.com/questions/16937076/how-does-one-use-a-custom-widget-with-a-generic-updateview-without-having-to-red
    """
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)



class SummariesCreateView(ModelFormWidgetMixin,CreateView):
    """
    class based view and file uploads:
    http://www.kelvinwong.ca/2013/09/19/upload-files-using-filefield-and-generic-class-based-views-in-django-1-5/
    https://godjango.com/35-upload-files/
    """
    model = Summaries
    fields = '__all__'
    #template_name = 'ZSIV/Summaries-create.html'
    widgets = {
        'SENT' : CheckboxInput,
        'Heftnummer' :  Select,
    }

class SummariesUpdateView(UpdateView):
    model = Summaries
    fields = '__all__'
    template_name = 'ZSIV/summaries_form.html' #  is the default
    widgets = {
        'SENT' : CheckboxInput,
        'Heftnummer' :  Select,
    }
    context_object_name = 'summary'
    

class SummariesDeleteView(DeleteView):
    model = Summaries
    fields = '__all__'
    model = Summaries
    widgets = {
        'SENT' : CheckboxInput,
        'Heftnummer' :  Select,
    }
    context_object_name = 'summary'
    def get_success_url(self):
        return reverse('ZSIV:summaries-index')




class TestFormstSetView(SortableListMixin,SearchableListMixin,ModelFormSetView):
    """
    Funktionierender MultiDeleteView
    extra views: 
    https://github.com/AndrewIngram/django-extra-views
    http://stackoverflow.com/questions/21105552/django-extra-views-and-sortablelistmixin-configuration-confusion
    """
    model = Summaries
    form_class = SummariesDeleteForm
    template_name = 'ZSIV/summaries_multidelete.html'
    delete = fields.BooleanField(required=False)
    fields = ["SENT","Journal","Jahrgang","Heftnummer"]
    print ()
    
    search_fields = ['SENT', 'Jahrgang']
    sort_fields_aliases = [('SENT', 'by_SENT'), ('id', 'by_id'), ]
    extra=0
    
    widgets = {
        'Heftnummer' :  Select(attrs={'disabled': 'disabled'}),
        'Jahrgang'   : Select(attrs={'disabled': 'disabled'}),
    }
    
"""
(3b) Listviews are VANIILLA list views!!
""" 
   
"""
 (4) Queue and send!
"""



class Queuelistview(ListView):
    """
    Die Quelistview soll die zu versendenden Emails schicken 
    Erbt von listview 

    Links:
    http://www.gregaker.net/2012/apr/20/how-does-djangos-class-based-listview-work/
    CBV documentation and reference!: 
    http://stackoverflow.com/questions/28400943/python-django-e-mail-form-example
    http://stackoverflow.com/questions/11268630/how-to-use-two-different-django-form-at-the-same-template
    reverse relations: 
    http://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    https://code.google.com/archive/p/django-selectreverse/
    Many to many and form: 
    http://stackoverflow.com/questions/21600192/django-form-for-many-to-many-model-how-do-i-fill-a-form-from-views-template
    http://stackoverflow.com/questions/11021242/accessing-many-to-many-through-relation-fields-in-formsets

    
    """
    def dispatch(self, request, *args, **kwargs):
        """
        see https://godjango.com/69-the-class-based-view/
        - Wann imemr asview benutzt wird, wird die dispatch Methode des Class based views aufgerufen
        - inspiziert was die request methode ist
        
        """
        #print (request.method)
        #print (self.http_method_names)
        #print (self._allowed_methods())
        return super(Queuelistview, self).dispatch(request, *args, **kwargs)
    
    
    
    def get_context_data(self, **kwargs):
        """
        http://stackoverflow.com/questions/16458006/django-access-context-in-template:
        default context variable for ListView is objects_list - oder doch mitarbeiter_list??
        context_object_name='all_mas' kann also rausgenommen werden
        
        Problem mit context
        http://lukeplant.me.uk/blog/posts/my-approach-to-class-based-views/
        no use to use get_context_data:
        http://reinout.vanrees.org/weblog/2014/05/19/context.html
        """
        # Call the base implementation first to get a context
        context = super(Queuelistview, self).get_context_data(**kwargs)
        context['emails']=self.emails # muss man die Mails zum Kontext hinzufügen??
        return context
    
    
    def get_queryset(self):
        """
        get_queryset ist die erste Methode die aufgerufen wird.
        darum wird die liste emails auch hier generiert 
        andere Methoden koennen die Liste dann so bekommen: 
        self.object_list = self.get_queryset() #  generiert emails mit: self.emails
        die Emaillistte soll überall zur Verfügung stehen, deswegen wird die nachher ungut umkopiert. 
        http://stackoverflow.com/questions/23402047/how-to-combine-two-querysets-when-defining-choices-in-a-modelmultiplechoicefield
        http://stackoverflow.com/questions/5629702/django-queryset-join-across-four-tables-including-manytomany
        """
        qs = super(Queuelistview,self).get_queryset()
        print ("modify qs when you want to contain only people with querysets!")
        mas = Mitarbeiter.objects.all()

        self.emails=[]
        for idxma, ma in enumerate(mas):
            
            subscriptions = ma.Subscriptions.filter(summaries__SENT=False).distinct()
            if not subscriptions:
                #context['emails'].append('')
                self.emails.append('')
                print ("\n no emails left for ", ma)
            else:
                tmpmail = mail.EmailMessage(
                            'Inhaltsverzeichnise Zeitschriften',
                            'Hallo Lieber Anwalt, da haste, Schüss von Frau Winkelmann',
                             settings.DEFAULT_FROM_EMAIL,
                             [ma.email]
                            )
                for idxsub, subsc in enumerate(subscriptions): # loop durch die JournalSubscriptions eines Mitarbeiters
                    #print (idxsub, subsc)
                    for summary in iter(subsc.summaries_set.iterator()): 
                        jn=str(summary.Journal).replace(' ','_')
                        hn=str(summary.Heftnummer)
                        jg=str(summary.Jahrgang)
                        ext = str(summary.Inhaltsverzeichnis).split('.')[-1]
                        attach_string = '_'.join([jn,jg,hn])+'.'+ext
                        fn=os.path.join(settings.MEDIA_ROOT,str(summary.Inhaltsverzeichnis))
                        tmpmail.attach_file(fn)
                        #tmpmail.attach(attach_string, summary.Inhaltsverzeichnis) #  mime type can be guessed "application/pdf"
                        print ("attaching file ", fn)
                
                print ("\n\nMITARBEITER NO ", idxma, " EMAIL: ",  ma.email)
            
                print ("no of substriptions for this MA: ",  len(subscriptions))
                #for x in tmpmail.attachments:
                #    print (x)
    
                self.emails.append(tmpmail)
        
        return qs

#    def get(self, request, *args, **kwargs):
#        
#        self.object_list = self.get_queryset() # generiert emails mit: self.emails
#        print("in der get methode")
#        print("debug punkt .. ")
        #return self.render_to_response(context)
    #    return HttpResponse('Hello World I am a get')



    def post(self, request, *args, **kwargs):
        """
        to do: send the email here. 
        After doing so, flat newly sent files as sent in SUMAARY. 
        redirect to success url or what?  
        
        self.object_list = self.get_queryset() ist von hier: 
        http://stackoverflow.com/questions/37675704/productlist-object-has-no-attribute-object-list
        
        
        sending mails:
        http://stackoverflow.com/questions/8659131/how-does-one-send-an-email-to-10-000-users-in-django
        """
        
        print ("")
        self.object_list = self.get_queryset() #  generiert emails mit: self.emails
        
        print ("SENDING .... ")
        if (1==1):
            connection = mail.get_connection()
            connection.open()
            
            for mamail in self.emails:
                print ("sending mail containing ",  len(mamail.attachments),  "attachments to ", mamail.recipients()[0])
                print (not mamail)
                mamail.send(
                            fail_silently=True
                            )
            
            connection.close()  
        Summaries.objects.filter(SENT=False).update(SENT=True)
        # Wohin?
        #return HttpResponse('I did the send')
        #return HttpResponseRedirect(reverse('ZSIV:index')) # zuruecl nach hause
        #return render_to_response('ZSIV/index.html') # zurueck nach hause
        return HttpResponseRedirect(reverse('ZSIV:queue'))



# 5) Experimental : Formset-Mixins udn so 


# Formset Example
""" 

https://github.com/epicserve/inlineformset-example/
formset example: Start to manipulate Journals
BookFormSet = inlineformset_factory(Author, Book, extra=0, min_num=1, fields=('title', ))

Autor hat mehrer Bücher
Journal hat mehrere Summaries

class Book(models.Model):
    author = models.ForeignKey(Author)

class AuthorCreateView(FormsetMixin, CreateView):
    template_name = 'books/author_and_books_form.html'
    model = Author
    form_class = AuthorForm
    formset_class = BookFormSet
    


class Summaries(models.Model):
    Journal = models.ForeignKey(Journals)

 """

from .forms import SummaryFormSet

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))



class JournalCreateView(FormsetMixin, CreateView):
    template_name = 'ZSIV/journal_and_summaries_form.html'
    model = Journals
    form_class = JournalForm
    formset_class = SummaryFormSet


# MAJViewIndex 
"""
Mixin, der die formfactory zum reinmixen von widgets erlauben soll
http://stackoverflow.com/questions/16937076/how-does-one-use-a-custom-widget-with-a-generic-updateview-without-having-to-red
"""
class modelformset_factory_Mixin(object):
    def get_form_class(self):
        return modelformset_factory(self.model, fields=self.fields, widgets=self.widgets,extra=1,exclude=("",))
    

class MAJViewIndex(TemplateResponseMixin, View,modelformset_factory_Mixin):
    template_name = 'ZSIV/ma_journal.html'
    fields = '__all__'
    #context_object_name = 'list_to_view'
    def get_queryset(self):
        #queryset = MAJournal.objects.filter(day__date=datetime.date.today())
        queryset = MAJournal.objects.filter()
        return queryset
    
    def dispatch(self, request, *args, **kwargs):
        print (request.method)
        print (self.http_method_names)
        print (self._allowed_methods())

        return super(MAJViewIndex, self).dispatch(request, *args, **kwargs)
        
    
    def post(self, request, *args, **kwargs):
        formset = self.FS(request.POST, request.FILES)

        if formset.is_valid():
            formset.save()
            formset = self.FS(queryset=self.queryset)

        else:
            formset = self.FS(queryset=self.queryset)

        return self.render_to_response({'formset':formset})
   

