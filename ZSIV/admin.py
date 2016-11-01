from django.contrib import admin
# Register your models here.


from .models import Journals
from .models import Mitarbeiter
from .models import MAJournal
from .models import Summaries
from ZSIV.models import Summaries





class majournalInline(admin.StackedInline):
    model=MAJournal
    extra=1
    
class MitarbeiterAdmin(admin.ModelAdmin):
    list_display = ('Vorname','Nachname','Anrede','email','Sex','id')
    inlines = [majournalInline]
admin.site.register(Mitarbeiter,MitarbeiterAdmin)


class JournalsAdmin(admin.ModelAdmin):
    list_display = ('Name','Kurztitel','Quelle','id')
    inlines = [majournalInline]
    extra=1
admin.site.register(Journals,JournalsAdmin)

class SummariesAdmin(admin.ModelAdmin):
    extra=1
admin.site.register(Summaries, SummariesAdmin)

