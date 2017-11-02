from django import forms
from .models import documento
from django import forms

class DocumentForm(forms.ModelForm):
    class Meta:
        model = documento
        fields = ('documento',)