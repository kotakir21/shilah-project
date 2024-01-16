import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateComplaintForm, AssignComplaintForm  # Update form imports
from .models import Complaint  # Update model import

User = get_user_model()

# cx can create a complaint from here 
def create_complaint(request):  # Rename the function
    if request.method == 'POST':
        form = CreateComplaintForm(request.POST)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.complaint_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.complaint_id = id
                    var.save()
                    # send email func
                    subject = f'{var.complaint_title} #{var.complaint_id}'
                    message = 'Thank you for creating a complaint, we will address it soon.'  # Update email message
                    email_from = 'cshilahkyatuhire@email.com'
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Your complaint has been submitted. We will address it soon.')  # Update success message
                    return redirect('customer-active-complaints')  # Update redirect
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-complaint')  # Update redirect
    else:
        form = CreateComplaintForm()  # Update form reference
        context = {'form': form}
        return render(request, 'complaint/create_complaint.html', context)  # Update template reference
            
# cx can see all active complaints
def customer_active_complaints(request):  # Rename the function
    complaints = Complaint.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'complaints': complaints}  # Update context
    return render(request, 'complaint/customer_active_complaints.html', context)  # Update template reference

# cx can see all resolved complaints
def customer_resolved_complaints(request):  # Rename the function
    complaints = Complaint.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'complaints': complaints}  # Update context
    return render(request, 'complaint/customer_resolved_complaints.html', context)  # Update template reference

# engineer can see all his/her active complaints
def engineer_active_complaints(request):  # Rename the function
    complaints = Complaint.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'complaints': complaints}  # Update context
    return render(request, 'complaint/engineer_active_complaints.html', context)  # Update template reference

# engineer can see all his/her resolved complaints
def engineer_resolved_complaints(request):  # Rename the function
    complaints = Complaint.objects.filter(engineer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'complaints': complaints}  # Update context
    return render(request, 'complaint/engineer_resolved_complaints.html', context)  # Update template reference

# assign complaints to engineers
def assign_complaint(request, complaint_id):  # Rename the function
    complaint = Complaint.objects.get(complaint_id=complaint_id)  # Update model reference
    if request.method == 'POST':
        form = AssignComplaintForm(request.POST, instance=complaint)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'Complaint has been assigned to {var.engineer}')
            return redirect('complaint-queue')  # Update redirect
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-complaint')  # Update redirect
    else:
        form = AssignComplaintForm(instance=complaint)  # Update form reference
        form.fields['engineer'].queryset = User.objects.filter(is_engineer=True)
        context = {'form': form, 'complaint': complaint}  # Update context
        return render(request, 'complaint/assign_complaint.html', context)  # Update template reference

# complaint details
def complaint_details(request, complaint_id):  # Rename the function
    complaint = Complaint.objects.get(complaint_id=complaint_id)  # Update model reference
    context = {'complaint': complaint}  # Update context
    return render(request, 'complaint/complaint_details.html', context)  # Update template reference

# complaint queue (for only admins)
def complaint_queue(request):  # Rename the function
    complaints = Complaint.objects.filter(is_assigned_to_engineer=False)  # Update model reference
    context = {'complaints': complaints}  # Update context
    return render(request, 'complaint/complaint_queue.html', context)  # Update template reference

def resolve_complaint(request, complaint_id):  # Rename the function
    complaint = Complaint.objects.get(complaint_id=complaint_id)  # Update model reference
    if request.method == 'POST':
        rs = request.POST.get('rs')
        complaint.resolution_steps = rs 
        complaint.is_resolved = True
        complaint.status = 'Resolved'
        complaint.save()
        messages.success(request, 'Complaint is now resolved and closed')
        return redirect('dashboard')  # Update redirect

