from django import forms
from .models import Journals, Summaries, MAJournal, Mitarbeiter
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

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



"""
https://docs.djangoproject.com/en/dev/topics/forms/formsets/#manually-rendered-can-delete-and-can-order
"""
from django.forms import fields     
from django.forms import widgets  
class SummariesDeleteForm(forms.ModelForm):
    
    id = fields.IntegerField(widget=widgets.HiddenInput)
    delete = fields.BooleanField(required=False)
    #Journal_id  = fields.IntegerField(widget=widgets.HiddenInput)
    #Heftnummer
    
    def save(self, commit=False):
        if self.is_valid() and self.cleaned_data['delete']:
            self.instance.delete()             
    #    def __init__(self, *args, **kwargs):
    #        self.user = kwargs.pop('user')
    #        super(SummariesDeleteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Summaries
        fields = '__all__'


#SummariesDeleteFormSet = inlineformset_factory(SummariesDeleteForm)