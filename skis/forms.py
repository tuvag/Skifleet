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


class MyPasswordResetForm(PasswordResetForm):
   def is_valid(self):
       email = self.data["email"]
       if sum([1 for u in self.get_users(email)]) == 0:
           self.add_error(None, "Unknown email; try again")
           return False
       return super().is_valid()