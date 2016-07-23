from django import forms
from .models import Journals, Summaries, MAJournal, Mitarbeiter
from django.forms import ModelForm

DISPLAY_CHOICES = (
    ("locationbox", "Display Location"),
    ("displaybox", "Display Direction")
)



class JournalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        http://www.pydanny.com/overloading-form-fields.html
        required field muss auf False gesetzt werden, sonst wird die Form ungueltig
        """
        super(JournalForm, self).__init__(*args, **kwargs)
        self.fields['Subscriptions'].required=False
    class Meta:
        model = Journals
        fields = '__all__'
        #fields = ['Subscriptions']
        widgets = {
            'Subscriptions': forms.CheckboxSelectMultiple,
        }
        
        
class MitarbeiterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """
        http://www.pydanny.com/overloading-form-fields.html
        """
        super(MitarbeiterForm, self).__init__(*args, **kwargs)
        self.fields['Subscriptions'].required=False

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
    