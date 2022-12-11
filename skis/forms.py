from django import forms
from .models import Ski, Setting, Technique, SkiTest
from django.contrib.auth.forms import PasswordResetForm
from betterforms.multiform import MultiModelForm
from django.contrib.admin.widgets import AdminDateWidget

""" class SkiForm(forms.ModelForm):

    class Meta:
        model = Ski
        fields = ('color_tag', 'ski_number', 'technique', 'grind', 'brand', 'img', 'notes' ) 
        labels = {
            'img': "Image",
        }

    def set_skiowner(self, User):
        self.ski_owner = User """

class SettingForm(forms.ModelForm):
    
    
    class Meta:
        model = Setting
        fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')
        #date = forms.DateField(label=('date'), widget=AdminDateWidget())

    def set_tester(self, User):
        self.tester = User

class SkiTestForm(forms.ModelForm):

    class Meta:
        model = SkiTest
        fields = ('ski', 'rank')

    #ski = forms.ModelMultipleChoiceField(queryset=Ski.objects.all())

class SettingCreationMultiForm(MultiModelForm):
    form_classes = {
        'setting': SettingForm,
        'ski1': SkiTestForm,
        'ski2': SkiTestForm,
        'ski3': SkiTestForm,
        'ski4': SkiTestForm,
        'ski5': SkiTestForm,
        'ski6': SkiTestForm,
        'ski7': SkiTestForm,
        'ski8': SkiTestForm,
    }


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
    """  search_technique =  forms.ModelChoiceField(
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

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=150)
    email = forms.EmailField(label='Email address', max_length=150)
    message = forms.CharField(label='Message',widget = forms.Textarea, max_length = 1000)
