from django import forms
from .models import documento
from django import forms

#Carga el formato del documento en la vista
class DocumentForm(forms.ModelForm):
    class Meta:
        model = documento
        fields = ('documento',)