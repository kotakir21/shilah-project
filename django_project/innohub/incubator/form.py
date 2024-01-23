from django import forms
from .models import Incubator

from django import forms
from .models import Incubator

class CreateincubatorForm(forms.ModelForm):
    class Meta:
        model = Incubator
        fields = [
            'incubator_title',
            'position_in_company',
            'applicant_name',
            'applicant_phone',
            'product_name',
            'problem_description',
            'solution_description',
            'serving_sectors',
            'competitors_description',
            'market_potential',
            'have_technical_documentation',
            'technical_documentation',
            'have_ursb_registration_number',
            'ursb_registration_number',
            'have_documented_processes',
            'documented_processes',
            'have_ura_registration_number',
            'ura_registration_number',
            'have_pdpo_registration_number',
            'pdpo_registration_number',
            'funding_amount',
            'hub_requirements',
        ]


class AssignincubatorForm(forms.ModelForm):
    class Meta:
        model = Incubator
        fields = ['officer']


