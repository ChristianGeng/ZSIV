
# Import the model classes we just wrote.


import django
django.setup()

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from ZSIV.models import Mitarbeiter, Journals, MAJournal, Choice, Question
from ZSIV.forms import JournalForm


''' Testing Amitarbeiter '''
Amitarbeiter = Mitarbeiter.objects.filter(id=1).select_related()
Amitarbeiter = Mitarbeiter.objects.select_related()
type(Amitarbeiter)
Amitarbeiter
Amitarbeiter = Mitarbeiter.objects.filter(pk=1).select_related()
type(Amitarbeiter)
Amitarbeiter
Amitarbeiter
Amitarbeiter.select_related().values()

mymitarbeiter = Amitarbeiter[0]
mymitarbeiter.majournal_set.select_related().values()


question = get_object_or_404(Question, pk=1)
len(question.choice_set.all())

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



question = get_object_or_404(Question, pk=1)
reverse('ZSIV:results', args=(question.id,))
HttpResponseRedirect(reverse('ZSIV:results', args=(question.id,)))
test = HttpResponseRedirect(reverse('ZSIV:results', args=(question.id,)))
test.items()

id=1
reverse('ZSIV:Summaries-update', args=(1,))


