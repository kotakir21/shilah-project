from django import forms
from .models import Ictsme


class CreateictsmeForm(forms.ModelForm):
    class Meta:
        model = Ictsme
        fields = [
            'ictsme_title',
            'position_in_company',
            'applicant_name',
            'applicant_phone',
            'product_name',
            'year_of_incorporation',
            'have_ursb_registration_number',
            'ursb_registration_number',
            'have_ura_registration_number',
            'ura_registration_number',
            'mentor_support',
            'hub_requirements',
        ]


class AssignictsmeForm(forms.ModelForm):
    class Meta:
        model = Ictsme
        fields = ['officer']
