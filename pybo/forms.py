from django import forms
from pybo.models import PreCard

TIME_CHOICES = [
    ('1차야자', '1차야자'),
    ('8교시', '8교시'),
    ('9교시', '9교시'),
]

class CardForm(forms.ModelForm):
    time = forms.MultipleChoiceField(choices=TIME_CHOICES,
                                     widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'type': 'checkbox'}))
    class Meta:
        model = PreCard
        fields = ['to', 'why', 'time', 'pw']
        widgets = {
            'to': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '특별실 명', 'id': 'name'}),
            'why': forms.TextInput(attrs={'class': 'form-control', 'id': 'why', 'placeholder': '사용 목적 및 사유'}),
            'pw': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pw', 'type': 'password', 'placeholder': '비밀번호'}),
        }
