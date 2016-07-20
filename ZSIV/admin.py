from django.contrib import admin
# Register your models here.

from .models import Question, Choice
from .models import Journals
from .models import Mitarbeiter
from .models import MAJournal
from .models import Summaries
from ZSIV.models import Summaries




class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3

# http://localhost:8000/admin/ZSIV/question/add/
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] 
    search_fields = ['question_text'] #  Django will search the question_text field. 
#admin.site.register(Question, QuestionAdmin)

class majournalInline(admin.StackedInline):
    model=MAJournal
    extra=1
    
class MitarbeiterAdmin(admin.ModelAdmin):
    list_display = ('Vorname','Nachname','email','id')
    inlines = [majournalInline]
admin.site.register(Mitarbeiter,MitarbeiterAdmin)


class JournalsAdmin(admin.ModelAdmin):
    list_display = ('Name','id')
    inlines = [majournalInline]
    extra=1
admin.site.register(Journals,JournalsAdmin)

class SummariesAdmin(admin.ModelAdmin):
    extra=1
admin.site.register(Summaries, SummariesAdmin)

