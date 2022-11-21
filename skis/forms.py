from django import forms
from .models import Ski, Skitest, Technique, Testski

class SkiForm(forms.ModelForm):

    class Meta:
        model = Ski
        fields = ('ski_number', 'technique', 'grind', 'brand', 'img', 'notes' ) 
        labels = {
            'img': "Image",
        }

    def set_skiowner(self, User):
        self.ski_owner = User