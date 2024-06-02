from django import forms
from pybo.models import PreCard

class CardForm(forms.ModelForm):
    class Meta:
        model = PreCard
        fields = [ 'to', 'why', 'time']
        widgets = {
            'to': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '특별실 명', 'id':'name'}),
            'why': forms.TextInput(attrs={'class': 'form-control', 'id':'why', 'placeholder': '사용 목적 및 사유'}),
            'time': forms.Select(attrs={'class': 'form-select', 'id':'when'})
        }