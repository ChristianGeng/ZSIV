from django import forms
from .models import Journals, Summaries, MAJournal, Mitarbeiter
from django.forms import ModelForm

DISPLAY_CHOICES = (
    ("locationbox", "Display Location"),
    ("displaybox", "Display Direction")
)



class JournalForm(ModelForm):
    class Meta:
        model = Journals
        fields = '__all__'
        #fields = ['Subscriptions']
        widgets = {
            'Subscriptions': forms.CheckboxSelectMultiple,
        }
        
        
class MitarbeiterForm(ModelForm):
    class Meta:
        model = Mitarbeiter
        fields = '__all__'
        #fields = ['Subscriptions']
        widgets = {
            'Subscriptions': forms.CheckboxSelectMultiple,
        }

class SummariesForm(ModelForm):
    class Meta:
        model = Summaries
        fields = '__all__'
        
        
class MAJournalForm(ModelForm):
    class Meta:
        model = MAJournal
        fields = '__all__'
    