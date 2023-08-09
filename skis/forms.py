from django import forms
from .models import Ski, Setting, Technique, SkiTest
from django.contrib.auth.forms import PasswordResetForm
from betterforms.multiform import MultiModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget
from datetime import datetime


class SettingForm(forms.ModelForm):
    
    class Meta:
        model = Setting
        fields = ('date', 'temprature', 'humidity', 'location', 'snow_type', 'notes')
        current_year = datetime.now().year
        widgets = {
            'date': SelectDateWidget(years=range(current_year - 20, current_year + 2)),
        }
        labels = {
            'date': 'When?',
        }
    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        if not self.instance.date:
            self.fields['date'].initial = datetime.today().date()

    def set_tester(self, User):
        self.tester = User

    # This form is only used as part of a SettingCreationMultiForm. 
    # The view handling that form is responsible for saving the model
    # created by this form directly, so the save() method here should 
    # not actually save the object. 
    def save(self, commit):
        return super().save(commit=False)

class SkiTestForm(forms.ModelForm):
    class Meta:
        model = SkiTest
        fields = ('ski', 'rank')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SkiTestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['ski'].queryset = Ski.objects.filter(ski_owner=user)

    # This form is only used as part of a SettingCreationMultiForm. 
    # The view handling that form is responsible for saving the model
    # created by this form directly, so the save() method here should 
    # not actually save the object. 
    def save(self, commit):
        return super().save(commit=False)
        

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SettingCreationMultiForm, self).__init__(*args, **kwargs)
        if user:
            for form_name in ['ski1', 'ski2', 'ski3', 'ski4', 'ski5', 'ski6', 'ski7', 'ski8']:
                self.forms[form_name].fields['ski'].queryset = Ski.objects.filter(ski_owner=user)

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
