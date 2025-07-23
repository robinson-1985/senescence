from django import forms
from .models import Cuidador

class CuidadorForm(forms.ModelForm):
    class Meta:
        model = Cuidador
        fields = '__all__'
