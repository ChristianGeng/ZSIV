import django
django.setup()
#from django.shortcuts import get_object_or_404
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
#Journals, MAJournal, Summaries

from django.core import mail


connection = mail.get_connection()
print(connection.connection)
print(connection.host)
connection.open()
            
tmpmail = mail.EmailMessage('subj', 'Test mail to jedhoo',to=['jedhoo@googlemail.com','jedhoo@web.de'])

# tmpmail.attach('test.pdf',myfilefield) # expected bytes-like object, not FieldFile
#myfilefield  = Summaries.objects.filter(SENT=False,Heftnummer=0).get().Inhaltsverzeichnis

#tmpmail.attach(filename, content, mimetype)
 
tmpmail.send(fail_silently=False)
print(tmpmail.attachments)
connection.close()
