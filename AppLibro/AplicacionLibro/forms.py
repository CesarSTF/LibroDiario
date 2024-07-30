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
        exclude = ['numeroComprobante', 'ivaIngreso', 'ivaEgreso', 'fecha', 'libroDiario']  # Excluye los campos
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción'}),
            'ingresoCaja': forms.NumberInput(attrs={'placeholder': 'Ingreso Caja'}),
            'egresoCaja': forms.NumberInput(attrs={'placeholder': 'Egreso Caja'}),
            'ingresoBanco': forms.NumberInput(attrs={'placeholder': 'Ingreso Banco'}),
            'egresoBanco': forms.NumberInput(attrs={'placeholder': 'Egreso Banco'}),
            'iva': forms.NumberInput(attrs={'placeholder': 'IVA (%)'})
        }
    iva = forms.DecimalField(max_digits=5, decimal_places=2, initial=0, label='IVA (%)')