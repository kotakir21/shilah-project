from django import forms
from .models import Ideation

class CreateideationForm(forms.ModelForm):
    class Meta:
        model = Ideation
        fields = [
            'ideation_title', 
            'applicant_name', 
            'applicant_phone', 
            'product_name',
            'position_in_company',
            'problem_description',
            'solution_description',
            'hub_requirements',
            ]

widgets = {
            'product_name': forms.TextInput(attrs={'required': False}),
            'position_in_company': forms.Select(attrs={'required': False}),
            'problem_description': forms.Textarea(attrs={'required': False}),
            'solution_description': forms.Textarea(attrs={'required': False}),
            'hub_requirements': forms.Textarea(attrs={'required': False}),
        }

class AssignideationForm(forms.ModelForm):
    class Meta:
        model = Ideation
        fields = ['officer']
