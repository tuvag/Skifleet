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
    search_text =  forms.CharField(
        required = False,
        label='Search name or surname!',
        widget=forms.TextInput(attrs={'placeholder': 'search here!'})
    )
