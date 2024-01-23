from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ictsme(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ictsmes_customer')
    officer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='ictsmes_officer', null=True, blank=True)
    ictsme_id = models.CharField(max_length=15, unique=True)
    ictsme_title = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=(('Active', 'Active'), ('Pending', 'Pending'), ('Resolved', 'Resolved')), default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=5, choices=(('A', 'A'), ('B', 'B')), default='B')
    is_assigned_to_officer = models.BooleanField(default=False)
    resolution_steps = models.TextField(blank=True, null=True)
    #ictsme specific fields
    position_in_company = models.CharField(
        max_length=20,
        choices=[
            ('Co-founder', 'Co-founder'),
            ('Founder', 'Founder'),
        ]
    )
    applicant_name = models.CharField(max_length=255)
    applicant_phone = models.CharField(max_length=15)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    year_of_incorporation = models.CharField(max_length=4, blank=True, null=True)
    have_ursb_registration_number = models.BooleanField(default=False)
    ursb_registration_number = models.CharField(max_length=50, blank=True, null=True)
    have_ura_registration_number = models.BooleanField(default=False)    
    ura_registration_number = models.CharField(max_length=50, blank=True, null=True)
    mentor_support = models.TextField(blank=True)
    hub_requirements = models.TextField(blank=True)


