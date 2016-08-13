import django

django.setup()
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ZSIV.models import Mitarbeiter, Journals, MAJournal, Summaries


from django.core import mail
import numpy as np

data = np.random.randint(10,size=1000)

Summaries.objects.filter(SENT=True).update(SENT=False)



connection = mail.get_connection()
print(connection.connection)
print(connection.host)
connection.open()
            
tmpmail = mail.EmailMessage('subj',
                            'Hallo Lieber Anwalt',
                            to=['jedhoo@googlemail.com']
                            )

# tmpmail.attach('test.pdf',myfilefield) # expected bytes-like object, not FieldFile
myfilefield  = Summaries.objects.filter(SENT=False,Heftnummer=0).get().Inhaltsverzeichnis



#tmpmail.attach(filename, content, mimetype)
 
tmpmail.send(fail_silently=False)
print(tmpmail.attachments)
connection.close()




''' Testing Amitarbeiter '''
Amitarbeiter = Mitarbeiter.objects.filter(id=1).select_related()
Amitarbeiter = Mitarbeiter.objects.select_related()
Amitarbeiter = Mitarbeiter.objects.filter(pk=1).select_related()
Amitarbeiter.select_related().values()
mymitarbeiter = Amitarbeiter[0]
mymitarbeiter.majournal_set.select_related().values()



journallist = Journals.objects.select_related()
journallist = Journals.objects.all()
journallist[1].majournal_set.values() 


journallist = Journals.objects.select_related()
for journal  in journallist: print(journal.majournal_set.all()) 
for journal  in journallist: print(journal.majournal_set.all().values()) 
journal.majournal_set.all().values()[0]['MA_id']
journal.majournal_set.all().values_list()
journal.majournal_set

journallist = Journals.objects.filter(pk=1).select_related()


test = Journals.objects.order_by('-Name')[:5]
type(test)
for journal  in journallist: print(journal.majournal_set.all().values())


# create some majournal thingies ...
majournal2add = MAJournal.objects.create(Journal_id=4, MA_id = 2)
majournal2add = MAJournal.objects.create(Journal_id=4, MA_id = 3)
majournal2add = MAJournal.objects.create(Journal_id=1, MA_id = 2)
majournal2add.save()

myselections = [1,2,4]
madata = MAJournal.objects.filter(Journal_id=1)
for x in myselections: madata.update_or_create(Journal_id=1, MA_id = x)

#madata.update_or_create(defaults)




# for journal in Journals.objects.all():  print (journal.id, journal.Name )
#     tmp  = Journals.objects.filter(id=journal.id).select_related() 
#     print (journal.id, journal.Name )

# for e in Mitarbeiter.objects.filter(id=1).select_related() 
#     print (e.Vorname)
# e.majournal_set.__dict__

mitarbeiter = get_object_or_404(Mitarbeiter, pk=1)
testma = get_object_or_404(Mitarbeiter, pk=1)

testma2 = Mitarbeiter.objects.get(pk=1)
type(testma2)



reverse('ZSIV:detailMA', args=(mitarbeiter.id,))
reverse('ZSIV:detailMA', args=(mitarbeiter.id,))
reverse('ZSIV:subscribe', args=(mitarbeiter.id,))




HttpResponseRedirect(reverse('ZSIV:detailMA', args=(mitarbeiter.id,)))




test = MAJournal.objects.all().select_related()






Summaries.objects.all()
test=Journals.objects.all().select_related().prefetch_related('Subscriptions')
test.query.__str__()




winner__lucky_draw_id=id



reverse('ZSIV:Summaries-update', args=(1,))
reverse('ZSIV:Summaries-detail', kwargs={'pk': 2})

get_object_or_404(Summaries, pk=1) 






from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
    
    

"""
im Model Entry:
blog = models.ForeignKey(Blog)
>>> b = Blog.objects.get(id=1)
>>> b.entry_set.all() # Returns all Entry objects related to Blog.
Summaries Model
   Journal = models.ForeignKey(Journals)
   
"""

q = Journals.objects.get(id=1)


"""
 TODO: Duerfen Heftnummer und Jahrgang leer sein???
 many to one relationship (nach): 
 jeder Reporter hat mehrere Artikel geschrieben
 das wird im Model "Article" als foreign key gehandelt
 reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
 
 
 jeder Reporter hat mehrere Artikel geschrieben
 das wird im Model "Article" als foreign key Reporter gehandelt
 reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
 
 
 jedes Journals hat  mehrere Summaries
 das wird im Model "Summaries" als foreign key Journal gehandelt
 
 
"""





"""
 noch nicht verschickte Summaries eines bestimmten Journals holen
"""
Summaries.objects.filter(SENT=False, Journal__Name='Wilderei und Unrecht')

"""
 zu einem noch nicht versandten Summary die Liste der Subscribers holen 
"""
q = Summaries.objects.filter(SENT=False)
mysummary=q[0]
mysummary.Journal.mitarbeiter_set.all()




"""
ein mitarbeiter kann mehrere Zeitschriften abonniert haben
Vin dieser Zeitschrift können meherre zu verschicken sein
"""

m = Mitarbeiter.objects.all()
mym = m[1] # ein Mitarbeiter
journalNo=2
summaries2sendforJournalALL = mym.Subscriptions.all()[journalNo].summaries_set.all()
summaries2sendforJournalUNSENT = mym.Subscriptions.all()[journalNo].summaries_set.filter(SENT=False)

for x in summaries2sendforJournalALL: print(x)
for x in summaries2sendforJournalUNSENT: print(x)


"""
http://stackoverflow.com/questions/21206319/django-model-relationships-in-views-and-templates?rq=1
http://stackoverflow.com/questions/5298535/django-traversing-multiple-successive-manytomany-relationships-in-templates-in
http://stackoverflow.com/questions/5298535/django-traversing-multiple-successive-manytomany-relationships-in-templates-in
"""

for ma in Mitarbeiter.objects.all():
    print("\n",ma.Vorname , ma.Nachname, ma.email)
    masumm = ma.Subscriptions.filter(summaries__SENT=False).all()
    for x in masumm: 
        print (x.summaries_set.filter(SENT=False))


"""
 Vielleicht: 
 related_name='from_employee'
 managed_by
 reverse = false?
"""

Summaries.objects.filter(SENT=False)
test = Summaries.objects.filter(SENT=False)








