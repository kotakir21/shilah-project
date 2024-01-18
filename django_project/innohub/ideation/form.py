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

class AssignideationForm(forms.ModelForm):
    class Meta:
        model = Ideation
        fields = ['engineer']
