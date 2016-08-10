from django.db import models
from django.contrib.sessions.base_session import AbstractBaseSession
import datetime   
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import uuid
import os



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
    #uploadLoc = filename
    ext = filename.split('.')[-1]
    uploadLoc = "%s.%s" % (uuid.uuid4(), ext)
    
    print ("uploading ", uploadLoc)
    return  uploadLoc

from django.conf import settings

def content_file_name(instance, filename):
#fn =  '/'.join(['content', instance.user.username, filename])
    ext = filename.split('.')[-1]
    # str(uuid.uuid4())
    #uploadLoc = "%s.%s" % (uuid.uuid4(), ext)
    journalname=instance.Journal.Name.replace(' ', '_')
    hn=str(instance.Heftnummer)
    jg=str(instance.Jahrgang)
    fn = '_'.join([journalname,jg,hn,str(uuid.uuid4())])+'.'+ext
    #uploadLoc = os.path.join(settings.MEDIA_ROOT,fn)
    uploadLoc=fn
    print("uploadLoc:" , uploadLoc)
    #print("fn:", fn)
    return uploadLoc

#upload_to=settings.MEDIA_ROOT


class Summaries(models.Model):
    Journal = models.ForeignKey(Journals)
    SENT = models.BooleanField(default=False)
    Jahrgang = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(2016,2031)])
    Heftnummer = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(55)])
    #file = models.FileField(upload_to=content_file_name)
    Inhaltsverzeichnis = models.FileField(upload_to=content_file_name,
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
