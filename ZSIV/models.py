from django.db import models
from django.contrib.sessions.base_session import AbstractBaseSession
import datetime   
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings 


class Mitarbeiter(models.Model):
    Vorname = models.CharField(max_length=200)
    Nachname = models.CharField(max_length=200)
    email = models.EmailField()
    Subscriptions = models.ManyToManyField('Journals', through='MAJournal') 
    def __str__(self):              # __unicode__ on Python 2
        return u'%s %s' % (self.Vorname, self.Nachname)

class Journals(models.Model):
    Name = models.CharField(max_length=400)
    Kurztitel = models.CharField(max_length=200,blank=True)
    Subscriptions = models.ManyToManyField('Mitarbeiter', through='MAJournal') # Note: Many to many fields beter referenced as  'Mitarbeiter' 
    def __str__(self):              # __unicode__ on Python 2
        return self.Name
    
class MAJournal(models.Model):
    MA = models.ForeignKey(Mitarbeiter)
    Journal = models.ForeignKey(Journals)
                                                    
    class Meta:
        unique_together = ('MA', 'Journal')

def upload_location(filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    #uploadLoc =  "%s/%s" %(instance.id, filename)
    uploadLoc = filename
    print ("uploading ", uploadLoc)
    return  uploadLoc
"""
 TODO: Duerfen Heftnummer und Jahrgang leer sein???
"""
class Summaries(models.Model):
    SENT = models.BooleanField(default=False)
    Journal = models.ForeignKey(Journals)
    Jahrgang = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(2016,2031)])
    Heftnummer = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(55)])
    Inhaltsverzeichnis = models.FileField(upload_to=settings.MEDIA_ROOT,
                          blank=False, 
                          default=False
                          )
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def was_created_recently(self):
        return self.Created >= timezone.now() - datetime.timedelta(days=1)
    def get_absolute_url(self): # fuer die adnub site, generiert im admin tool "view on site"
        #return reverse('ZSIV:Summaries-detail', kwargs={'pk': self.pk})
        return reverse('ZSIV:summaries-index')
        #return reverse('ZSIV:Summaries-detail', args=(Summaries.id,))
    def __str__(self):
        return str(self.Journal)+', Jg. '+str(self.Jahrgang)+', No. '+str(self.Heftnummer)+', sent: '+str(self.SENT)
    class Meta:
        unique_together = ("Journal","Heftnummer","Jahrgang")
