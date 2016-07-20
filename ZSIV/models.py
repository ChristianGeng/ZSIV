
from django.db import models

from django.contrib.sessions.base_session import AbstractBaseSession
import datetime   
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
#from  . import  *
#from MySQLdb.constants.FIELD_TYPE import YEAR
# import datetime
# from django.db import models
# from django.utils import timezone
# Create your models here.


class Mitarbeiter(models.Model):
    Vorname = models.CharField(max_length=200)
    Nachname = models.CharField(max_length=200)
    email = models.EmailField()
    Subscriptions = models.ManyToManyField('Journals', through='MAJournal') 
    
    #def Journals(self):
    #    return self.objects.select_related('Journal_id')
    
    def __str__(self):              # __unicode__ on Python 2
        return u'%s %s' % (self.Vorname, self.Nachname)


class Journals(models.Model):
    Name = models.CharField(max_length=400)
    Kurztitel = models.CharField(max_length=200,blank=True)
    Subscriptions = models.ManyToManyField('Mitarbeiter', through='MAJournal') # Note: Many to many fields beter referenced as  'Mitarbeiter' 
    
    #models.ManyToManyField(Jou
    #def Mitarbeiter(self):
    #    return self.objects.select_related('MA_id')
    
    def __str__(self):              # __unicode__ on Python 2
        return self.Name
    
class MAJournal(models.Model):
    MA = models.ForeignKey(Mitarbeiter)
    Journal = models.ForeignKey(Journals)
                                                    
    class Meta:
        unique_together = ('MA', 'Journal',)
        

from django.conf import settings 

def upload_location(filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    #uploadLoc =  "%s/%s" %(instance.id, filename)
    uploadLoc = filename
    print ("uploading ", uploadLoc)
    return  uploadLoc


class Summaries(models.Model):
    SENT = models.BooleanField(default=False)
    Journal = models.ForeignKey(Journals)
    Jahrgang = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(2016,2031)])
    Heftnummer = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(55)])
    
    #Filename = models.CharField(max_length=400)
    Inhaltsverzeichnis = models.FileField(upload_to=settings.MEDIA_ROOT,
                          blank=False, 
                          default=False
                          )
    
    
    #logo = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='logos', default='settings.MEDIA_ROOT/logos/anonymous.jpg')
    
    #OLD CreationDate = models.DateTimeField(default=timezone.now(), blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    #PublicationDate = models.DateField(default = datetime.datetime(1901, 1, 1))
    #Volume = models.PositiveSmallIntegerField(blank=True, null=True)
    
    
    def was_created_recently(self):
        return self.Created >= timezone.now() - datetime.timedelta(days=1)
    def get_absolute_url(self): # fuer die instance based views, generiert im admin tool "view on site"
        return reverse('ZSIV:Summaries-detail', kwargs={'pk': self.pk})
        

    def __str__(self):
        return str(self.Journal)+', Jg. '+str(self.Jahrgang)+', No. '+str(self.Heftnummer)

# # jede class variable ist ein database field aka spalte
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
# 
#     def __str__(self):
#         return self.question_text
# 
#     def was_published_recently(self):
#         # alte Version ist nicht durch den test gekommen. 
#         # zukuenftige Daten ergaben auch ein gueltiges ergebnis
#         #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#         # jetzt:
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#     # additional improvement. Verbessern die die Headers in der admin page aussehen
#     was_published_recently.admin_order_field = 'pub_date' # sortieren ermoeglichen 
#     was_published_recently.boolean = True # gruenes haekchen
#     was_published_recently.short_description = 'Published recently?' # ueberschrift
# 
# 
# # optionales erstes argument: Question in diesem Fall: gut lesbarer identifier
# 
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text
#     #Sent = models.S    