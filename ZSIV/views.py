from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Journals
from .models import MAJournal
from .models import Mitarbeiter
from .models import Summaries
from .models import MessageText

#from .forms import SummariesDeleteFormSet, 
from .forms import SummariesDeleteForm
from .forms import JournalForm
from .forms import MessageTextForm
from django.views.generic.edit import FormView
from ZSIV.forms import MitarbeiterForm
from django.forms import modelformset_factory
from django.forms.widgets import CheckboxInput, Select
from django.forms.models import modelform_factory
from django.forms import fields

from django.shortcuts import  render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings


from django.views import generic
from django.views.generic import ListView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from extra_views import ModelFormSetView
from extra_views import SearchableListMixin
from extra_views import SortableListMixin
from django.views.generic.base import  TemplateResponseMixin, View
# two ways to import: from django.views.generic import View

#from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy

#from django.forms.widgets import HiddenInput

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

Registration
# Django Tutorial for Beginners - 34 - User Registration https://www.youtube.com/watch?v=3UEY0ZIQ9dU
# https://docs.djangoproject.com/en/1.10/topics/auth/default/#auth-web-requests #
# https://django-registration-redux.readthedocs.io/en/latest/quickstart.html

"""


from contextlib import contextmanager
import threading
import _thread

class TimeoutException(Exception):
    """
    Timeouts, um einen Email timeout zu behandeln
    http://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
    
    import time
    ends after 5 seconds
    with time_limit(5, 'sleep'):
        for i in range(10):
            time.sleep(1)
        
    """
    def __init__(self, msg=''):
        self.msg = msg

@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()       

    

""" (1) Main Page """
#def index(request):
#    return render_to_response('ZSIV/index.html')


def indexView(request):
    #return render_to_response('ZSIV/index.html')
    # man muss den context mit uebergeben
    # see: http://stackoverflow.com/questions/30559020/django-login-template-doesnt-recognize-logged-user
    return render(request, 'ZSIV/index.html', {})


class MyView(View,LoginRequiredMixin):
    def get(self, request):
        print("MyView ",request.user.is_authenticated())
        #return render_to_response('ZSIV/index.html')
        return render(request, 'ZSIV/index.html', {})

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


#from django.contrib.auth.decorators import login_required
#@login_required   
def MA_Subscribe_Journals(request, mitarbeiter_id): 
    """
    Die Journals eines einzelnen Mitarbeiters - aus  der Liste aller Journals
    """
    formTemplate = 'ZSIV/ma_subscribe_journal.html'
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
    
    formTemplate = 'ZSIV/journal_subscribe_ma.html'
    journallist = Journals.objects.filter(pk=journal_id).select_related()
    myjournal = journallist[0] # TODO: pk lookup always first instance
    
    # linking table
    ma_journal_data = MAJournal.objects.filter(Journal_id=journal_id)
    initialvalues = [x['MA_id'] for x in myjournal.majournal_set.values()]
    if request.method == 'POST':
        form = JournalForm(request.POST, 
                           initial={'Subscriptions': initialvalues}, 
                           instance=myjournal,
                           )
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
    template_name = 'ZSIV/summaries_add.html'
    widgets = {
        'SENT' : CheckboxInput,
        'Heftnummer' :  Select,
    }


    
    
class SummariesUpdateView(UpdateView):
    model = Summaries
    fields = '__all__'
    template_name = 'ZSIV/summaries_update.html' 
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
    
    search_fields = ['SENT', 'Jahrgang']
    sort_fields_aliases = [('SENT', 'by_SENT'), ('id', 'by_id'), ]
    extra=0
    
    widgets = {
        'Heftnummer' : Select(attrs={'disabled': 'disabled'}),
        'Jahrgang'   : Select(attrs={'disabled': 'disabled'}),
    }
    
"""
(3b) Listviews are VANIILLA list views!!
""" 
   
"""
 (4) Queue and send, und der Email Text 
"""

class MessageTextView(FormView):
    form_class = MessageTextForm
    model = MessageText
    template_name = 'ZSIV/MessageText.html'
# geht nicht: 
#    widgets = {
#        'text' : Textarea(attrs={'size' : '1'}), # TextField 'cols': '40', 'rows': '10'
#        'subject'   : Textarea(attrs={'cols': '4', 'rows': '10'}), # CharField
#    }
    
    
    def get_initial(self):
        """ 
        http://stackoverflow.com/questions/19479064/how-to-set-form-field-value-django
        """
        mt  = MessageText.load()
        return {'text': mt.text, 'subject' : mt.subject }
    
    
    def dispatch(self, request, *args, **kwargs):
        """
        see https://godjango.com/69-the-class-based-view/
        - Wann imemr asview benutzt wird, wird die dispatch Methode des Class based views aufgerufen
        - inspiziert was die request methode ist
        
        """
        #print (request.method)
        #print (self.http_method_names)
        #print (self._allowed_methods())
        return super(MessageTextView, self).dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('ZSIV:MessageText')
    
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
        qs = super(MessageTextView,self).get_queryset()
        return qs

    def form_valid(self, form):
            form.save(commit = True)
            return super(MessageTextView, self).form_valid(form)





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
        context['journalName']= self.journalName
        context['journalQuelle']= self.journalQuelle
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
        
        def htmlify(text):
            return  "<html><body><pre>"+text+"</pre></body></html>"
        
        
        mt  = MessageText.load() # load email text and subject
        grussfloskel = "Sehr geehrte"
        
        qs = super(Queuelistview,self).get_queryset()
        print ("modify qs when you want to contain only people with querysets!")
        print("Emails werden gesendet von  ",settings.DEFAULT_FROM_EMAIL)
        mas = Mitarbeiter.objects.all()

        self.emails=[]
        self.journalName=[]
        self.journalQuelle=[]
        for idxma, ma in enumerate(mas):
            
            subscriptions = ma.Subscriptions.filter(summaries__SENT=False).distinct()
            if not subscriptions:
                self.emails.append('')
                # print ("\n no emails left for ", ma)
            else:

                grussfloskeluse = grussfloskel
                if ma.Sex=='m': grussfloskeluse = grussfloskel+"r"
                anrede = " ".join([ grussfloskeluse, ma.Anrede, ma.Nachname+","])
                mailtext = "{0}\r\n\r\n  {1}".format(anrede, mt.text) +'\r\n\r\n'
                mailtext =   mailtext + "\r\n"+ "\r\n"  + "Quelle(n):\r\n\r\n"
                
                tmpmail = mail.EmailMultiAlternatives(
                            mt.subject,
                            mailtext,
                             settings.DEFAULT_FROM_EMAIL,
                             [ma.email]
                            )
                
                #tmpmail.attachments.JournalName=[]
                #tmpmail.attachments.JournalQuelle=[]

                for idxsub, subsc in enumerate(subscriptions): # loop durch die JournalSubscriptions eines Mitarbeiters
                    for summary in iter(subsc.summaries_set.iterator()): 
                        fn=os.path.join(settings.MEDIA_ROOT,str(summary.Inhaltsverzeichnis))
                        tmpmail.attach_file(fn)
                        journalData = Journals.objects.get(Name=str(summary.Journal.Name))
                        #tmpmail.attachments.JournalName.append(journalData.Name)
                        #tmpmail.attachments.JournalQuelle.append(journalData.Quelle)
                        
                        
                        mailtext =   mailtext + journalData.Name + " - " + journalData.Quelle + "\r\n" 
                
                
                
                mailhtml = htmlify(mailtext)
                tmpmail.attach_alternative(mailhtml, "text/html")
                self.emails.append(tmpmail)
                self.journalName.append(journalData.Name)
                self.journalQuelle.append(journalData.Quelle)
                
        
        return qs

#    def get(self, request, *args, **kwargs):
#        
#        self.object_list = self.get_queryset() # generiert emails mit: self.emails
#        print("in der get methode")
#        print("debug punkt .. ")
#        return self.render_to_response(context)
#       return HttpResponse('Hello World I am a get')



    def post(self, request, *args, **kwargs):
        """
        to do: send the email here. 
        After doing so, flat newly sent files as sent in SUMAARY. 
        redirect to success url or what?  
        
        self.object_list = self.get_queryset() ist von hier: 
        http://stackoverflow.com/questions/37675704/productlist-object-has-no-attribute-object-list
        
        
        sending mails:
        http://stackoverflow.com/questions/8659131/how-does-one-send-an-email-to-10-000-users-in-django
        Threaded Sending: 
        http://stackoverflow.com/questions/32979945/django-send-mail-function-taking-several-minutes
        
        Wichtiges Feature hier: 
        Logging: Wenn email-versand fehlschlägt, dann soll der Logger das in den Log File Schreiben
        Python logging configuration
        Loggers: 
            Ein Bucket, in den Logging-Messages geschrieben werden koennen
        Handlers:
            Was passiert mit jeder Message in einem Logger
        Filter: 
            Welche Logeintraege gelangen vom Logger zum Handler
        Formatters:
            Die machen was man denkt - Formattieren
        Der Standardplatz für einen Logger ist settings.py
            
        
        """
        
        #FALSCH
        #try:
        #        send_mail(subject, message, sender, recipients)
        #    except smtplib.SMTPException:
        #        result = smtplib.SMTPException.message
        #RICHTIG    
        #try:
        #    send_mail(subject, message, sender, recipients)
        #except smtplib.SMTPException as e:
        #result = str(e)
      
        # from email_validator import validate_email, EmailNotValidError, EmailUndeliverableError
        import logging
        logger = logging.getLogger("django")
        import smtplib
        import sys
        from django.http import HttpResponse
        
        print ("")
        self.object_list = self.get_queryset() #  generiert emails mit: self.emails
        
        try:
            connection = mail.get_connection()
            connection.open()
            print("connection offen!")
            logger.info("Successfully opened email connection")
        except smtplib.SMTPException as e:
            msg = str(e)
            #logger.error("Houston, we have a %s", "major problem: %s", exc_info=1, str(e))
            logger.error("smtp fehler")
            return HttpResponse(msg)
        except: # https://docs.python.org/3/tutorial/errors.html
            logger.error("ein anderer Fehler")
            return HttpResponse("ein anderer Fehler")
            
        
            
        
        for mamail in self.emails:
            print(type(mamail))
            print ("debug the fuck")
            print ("debug")
            print(str(mamail))
            if  isinstance(mamail,mail.message.EmailMultiAlternatives):
                msg = "EMAIL: attempting to send email containing "+str(len(mamail.attachments))+" attachments to "+"\n".join(mamail.to)
                logger.info(msg)
                with time_limit(40, 'sleep'):
                    try: 
                        #validation = validate_email("\n".join(mamail.to))
                        msg = mamail.send(fail_silently=False)
                        if msg == 1:
                            logmessage = " EMAIL SUCCESS: sent mail to "+"\n".join(mamail.to)
                            logger.info(logmessage) # gibt 1 ween success
                                                    # The return value will be the number of successfully delivered messages.
                                                    # https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
                    except EmailNotValidError as e:
                        #errno, strerror = e.args
                        logger.error("EMAIL: EmailNotValidError")
                        pass
                    except EmailUndeliverableError as e:
                        errno, strerror = e.args
                        logger.error("EMAIL: EmailUndeliverableError:({0}): {1}".format(errno,strerror))
                        pass
                    except TimeoutException as e:
                        errno, strerror = e.args
                        logger.error("EMAIL: TimeoutException({0}): {1}".format(errno,strerror))
                        print("Timeout Exception??")
                        pass
                    except: 
                        #raise Exception('Unknown Christian error ') # use raise to raise  your own errors.
                        logger.error('EMAIL : Unknown Christian error ')
                        print("andere Exception?")
                        pass 
            else:
                msg = "EMAIL: no emails to send!"
                #logger.info(msg)
                
            
        connection.close()  
        
            
        #Summaries.objects.filter(SENT=False).update(SENT=True)
        
        #except Exception as e:
            #logger.exception('Exception when sending emails!!!')
        #    print('Exception when sending emails!!!')
        
        
        
        
        
        # Wohin?
        #return HttpResponse('I did the send')
        #return HttpResponseRedirect(reverse('ZSIV:index')) # zuruecl nach hause
        #return render_to_response('ZSIV/index.html') # zurueck nach hause
        return HttpResponseRedirect(reverse('ZSIV:queue'))



# 5) registration / auth
""" user registration """
from django.contrib.auth import authenticate, login
from .forms import UserForm

class UserFormView(View):
    form_class = UserForm
    template_name = 'ZSIV/registration_form.html'

    # display blank form (neuer user kommt zum account, soll er dürfen)
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form' : form})
    
    def post(self,request):
        form = self.form_class(request.POST) # die post data sind schon validiert
        if form.is_valid():
            user = form.save(commit=False) # eine Objekt aus der form erzeugen, noch nicht in die DB speichern 
            # cleaned / normalized data 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('ZSIV:index')
            
        return render(request, self.template_name,{'form' : form})
            




"""
(6) Manage Journals
"""

class JournalCreateView(CreateView):
    model = Journals
    fields = ["Name","Kurztitel","Quelle"]
    template_name = 'ZSIV/journal_add.html' #  is the default
    # TODO: redirect
    #def get_success_url(self):
    #    return reverse('ZSIV:summaries-index')

class JournalListview(ListView):
    model = Journals
    fields = ["Name","Kurztitel","Quelle"]
    context_object_name = 'list_to_view'
    template_name="ZSIV/journal_list_EditingView.html"
    def get_context_data(self, **kwargs):
        context = super(JournalListview, self).get_context_data(**kwargs)
        return context

class JournalUpdateView(UpdateView):
    model = Journals
    fields = ["Name","Kurztitel","Quelle"]
    template_name = 'ZSIV/journal_update.html' #  is the default
    context_object_name = 'Journal'   

class JournalDeleteView(DeleteView):
    model = Journals
    success_url = reverse_lazy('ZSIV:Journal-List')
    context_object_name = 'Journal'  
    template_name = 'ZSIV/journal_confirm_delete.html' 

"""
(7) Manage Mitarbeiter
"""

class MitarbeiterCreateView(CreateView):
    model = Mitarbeiter
    fields = ["Vorname","Nachname","Sex","Anrede","email"]
    template_name = 'ZSIV/mitarbeiter_add.html' #  is the default

class MitarbeiterListview(ListView):
    model = Mitarbeiter
    context_object_name = 'list_to_view'
    template_name="ZSIV/mitarbeiter_list_EditingView.html"
    def get_context_data(self, **kwargs):
        context = super(MitarbeiterListview, self).get_context_data(**kwargs)
        return context

class MitarbeiterUpdateView(UpdateView):
    model = Mitarbeiter
    fields = ["Vorname","Nachname","Sex","Anrede","email"]
    template_name = 'ZSIV/mitarbeiter_update.html'
    context_object_name = 'Mitarbeiter'


class MitarbeiterDeleteView(DeleteView):
    model = Mitarbeiter
    success_url = reverse_lazy('ZSIV:Mitarbeiter-List')
    context_object_name = 'Mitarbeiter'
    








            
# (XXXX) Experimental : Formset-Mixins  so 


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
   

