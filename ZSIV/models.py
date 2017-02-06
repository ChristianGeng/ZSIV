
from django.db import models
import datetime   
from django.utils import timezone
from django.core.urlresolvers import reverse
import uuid
#from django.template.defaultfilters import default

class SingletonModel(models.Model):
    """
    https://goodcode.io/articles/django-singleton-models/
    Singleton Django Model
    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.
    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.
    Useful for things like system-wide user-editable settings.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class MessageText(SingletonModel):
    subject = models.CharField(max_length=1000)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

SEX_CHOICES = (
    ('m', 'männlich'),
    ('f', 'weiblich'),
)


class Mitarbeiter(models.Model):
    Vorname = models.CharField(max_length=200)
    Nachname = models.CharField(max_length=200)
    Anrede = models.CharField(max_length=200,default="Frau Dr. ")
    Sex = models.CharField(max_length=10, choices = SEX_CHOICES , default="f")
    email = models.EmailField()
    Subscriptions = models.ManyToManyField('Journals', through='MAJournal') 
    def __str__(self):              # __unicode__ on Python 2
        return u'%s %s' % (self.Vorname, self.Nachname)
    def get_absolute_url(self): # fuer die admin site, generiert im admin tool "view on site"
        return reverse('ZSIV:Mitarbeiter-List')
    class Meta:
        unique_together = ("Vorname","Nachname","email")


QUELLE_CHOICES = (
    ('unspecified', 'unspecified'),
    ('Juris', 'Juris'),
    ('BeckOnline', 'Beck Online'),
    ('Volltext', 'Volltext'),
    ('Printausgabe', 'Printausgabe'),
    ('Jurion', 'Jurion'),
)


class Journals(models.Model):
    Name = models.CharField(max_length=200,blank=False) # https://wildlyinaccurate.com/mysql-specified-key-was-too-long-max-key-length-is-767-bytes/
    Kurztitel = models.CharField(max_length=50,blank=False)
    Quelle = models.CharField(max_length=200, choices = QUELLE_CHOICES, default='Printausgabe')
    
    Subscriptions = models.ManyToManyField('Mitarbeiter', through='MAJournal') # Note: Many to many fields beter referenced as  'Mitarbeiter' 
    def __str__(self):              # __unicode__ on Python 2
        return self.Name
    def get_absolute_url(self): # fuer die admin site, generiert im admin tool "view on site"
        return reverse('ZSIV:Journal-List')
    class Meta:
        unique_together = ("Name","Kurztitel")
        
    
class MAJournal(models.Model):
    MA = models.ForeignKey(Mitarbeiter)
    Journal = models.ForeignKey(Journals)
                                                    
    class Meta:
        unique_together = ('MA', 'Journal')


def upload_location(filename):
    """
    Darf nicht gelöscht werden, sonst meckern alte Migrations. 
    """
    ext = filename.split('.')[-1]
    uploadLoc = "%s.%s" % (uuid.uuid4(), ext)
    return  uploadLoc



def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    journalname=instance.Journal.Name.replace(' ', '_')
    hn=str(instance.Heftnummer)
    jg=str(instance.Jahrgang)
    fn = '_'.join([journalname,jg,hn,str(uuid.uuid4())])+'.'+ext
    uploadLoc=fn
    print("uploadLoc:" , uploadLoc)
    return uploadLoc




class Summaries(models.Model):
    Journal = models.ForeignKey(Journals)
    SENT = models.BooleanField(default=False)
    Jahrgang = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(2016,2031)])
    Heftnummer = models.PositiveSmallIntegerField(blank=True, null=True, choices = [(i,i) for i in range(55)])
    Inhaltsverzeichnis = models.FileField(upload_to=content_file_name,
                          blank=False, 
                          default=False
                          )
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def was_created_recently(self):
        return self.Created >= timezone.now() - datetime.timedelta(days=1)
    def get_absolute_url(self): # fuer die admin site, generiert im admin tool "view on site"
        return reverse('ZSIV:summaries-index')
    def __str__(self):
        return str(self.Journal)+', Jg. '+str(self.Jahrgang)+', No. '+str(self.Heftnummer)+', sent: '+str(self.SENT)
    class Meta:
        unique_together = ("Journal","Heftnummer","Jahrgang")
