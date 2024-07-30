from django import forms
from .models import LibroDiario, EntradaDiario

class LibroDiarioForm(forms.ModelForm):
    class Meta:
        model = LibroDiario
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class EntradaDiarioForm(forms.ModelForm):
    class Meta:
        model = EntradaDiario
        exclude = ['numeroComprobante', 'ivaIngreso', 'ivaEgreso']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
