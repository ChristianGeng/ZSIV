from django import forms
from .models import Journals, Summaries, Mitarbeiter, MessageText
from django.forms import ModelForm
from django.forms.models import inlineformset_factory


class MessageTextForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageTextForm,self).__init__(*args, **kwargs)
    class Meta:
        model=MessageText
        fields='__all__'
        
        
    


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


        
        








"""
https://docs.djangoproject.com/en/dev/topics/forms/formsets/#manually-rendered-can-delete-and-can-order
"""
from django.forms import fields     
from django.forms import widgets  
class SummariesDeleteForm(forms.ModelForm):
    #readonly_fields = ('Heftnummer')
    id = fields.IntegerField(widget=widgets.HiddenInput)
    delete = fields.BooleanField(required=False)
        
    def save(self, commit=False):
        if self.is_valid() and self.cleaned_data['delete']:
            self.instance.delete()             
    #    def __init__(self, *args, **kwargs):
    #        self.user = kwargs.pop('user')
    #        super(SummariesDeleteForm, self).__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs): 
        super(SummariesDeleteForm, self).__init__(*args, **kwargs)
        self.fields['Journal'].disabled = True
        self.fields['SENT'].disabled = True
        
    class Meta:
        model = Summaries
        fields = '__all__'
        

"""  Versuch eines Journal Multidelete views mittels inlineformset """        
SummaryFormSet = inlineformset_factory(Journals,Summaries, extra=0, fields=('Jahrgang','Heftnummer', ))
