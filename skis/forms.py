from django import forms
from .models import Ski, Setting, Technique, SkiTest
from django.contrib.auth.forms import PasswordResetForm

class SkiForm(forms.ModelForm):

    class Meta:
        model = Ski
        fields = ('ski_number', 'technique', 'grind', 'brand', 'img', 'notes' ) 
        labels = {
            'img': "Image",
        }

    def set_skiowner(self, User):
        self.ski_owner = User

class SettingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d%m%Y'),input_formats=['%d%m%Y'])
    
    class Meta:
        model = Setting
        fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')

    def set_tester(self, User):
        self.tester = User


class MyPasswordResetForm(PasswordResetForm):
   def is_valid(self):
       email = self.data["email"]
       if sum([1 for u in self.get_users(email)]) == 0:
           self.add_error(None, "Unknown email; try again")
           return False
       return super().is_valid()



class SkiSearchForm(forms.Form):
    search_ski =  forms.CharField(
        required = False,
        label='Search:',
        widget=forms.TextInput(attrs={'placeholder': 'Ski details'})
    )
    """ search_technique =  forms.ModelChoiceField(
        required = False,
        widget=forms.ModelChoiceField(queryset=Technique)
    ) """

class SettingSearchForm(forms.Form):
    search_text =  forms.CharField(
        required = False,
        label='Search:',
        widget=forms.TextInput(attrs={'placeholder': 'Testing details'})
    )
    search_temprature = forms.IntegerField(
                    required = False,
                    label='Temprature'
                  )
    search_date = forms.DateField(
                    required = False,
                    label='Date',
                    widget=forms.NumberInput(attrs={'type': 'date'})
                  )

