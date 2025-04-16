from django import forms
from .models import ASRequest

class ASRequestForm(forms.ModelForm):

    class Meta:
        model = ASRequest
        fields = ['symptom', 'detail', 'submitter']
        widgets = {
            'symptom': forms.Select(attrs={
                'onchange': 'toggleContentField()',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'detail': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'submitter': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'
            }),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['symptom'].empty_label = '현재 증상을 선택해주세요'
            

