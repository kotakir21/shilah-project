from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Complaint(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_customer')
    officer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='complaints_officer', null=True, blank=True)
    complaint_id = models.CharField(max_length=15, unique=True)
    complaint_title = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=(('Active', 'Active'), ('Pending', 'Pending'), ('Resolved', 'Resolved')), default='Pending')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=5, choices=(('A', 'A'), ('B', 'B')), default='B')
    is_assigned_to_officer = models.BooleanField(default=False)
    resolution_steps = models.TextField(blank=True, null=True)
    #complaint specific fields
    complainant_name = models.CharField(max_length=255)
    complainant_phone = models.CharField(max_length=15)
    is_submitted_for_another = models.BooleanField(default=False)
    other_innovator_name = models.CharField(max_length=255, blank=True, null=True)
    other_innovator_contact = models.CharField(max_length=15, blank=True, null=True)
    complaint_details = models.TextField(blank=True)
    is_first_time_submission = models.BooleanField(default=False)
    additional_information = models.TextField(blank=True, null=True)

