from django import forms
from .models import Complaint

class CreateComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'complaint_title', 
            'complainant_name', 
            'complainant_phone', 
            'is_submitted_for_another',
            'other_innovator_name',
            'other_innovator_contact',
            'complaint_details',
            'is_first_time_submission',
            'additional_information',
            ]

class AssignComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['officer']
