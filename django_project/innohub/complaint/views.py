import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateComplaintForm, AssignComplaintForm
from .models import Complaint

User = get_user_model()

# cx can create a complaint from here 
def create_complaint(request):
    if request.method == 'POST':
        form = CreateComplaintForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.complaint_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.complaint_id = id
                    var.save()

                    # Send email to customer
                    subject_customer = f'complaint Submitted Successfully - #{var.complaint_id}'
                    message_customer = 'Thank you for creating a complaint. A Support officer will be assigned soon.'
                    email_from_customer = 'your-email@example.com'  # Replace with your email
                    recipient_list_customer = [request.user.email]
                    send_mail(subject_customer, message_customer, email_from_customer, recipient_list_customer)

                    # Send email to admin
                    subject_admin = f'New complaint Submitted - #{var.complaint_id}'
                    message_admin = f'A new complaint has been submitted by {request.user.email}. complaint ID: {var.complaint_id}'
                    email_from_admin = 'kbobroberts@gmail.com'  # Replace with your email
                    recipient_list_admin = ['kotakirobert7@gmail.com']  # Replace with the actual admin email
                    send_mail(subject_admin, message_admin, email_from_admin, recipient_list_admin)

                    messages.success(request, 'Your complaint has been submitted. A Support officer will be assigned soon.')
                    return redirect('customer-active-complaints')

                except IntegrityError:
                    continue

            else:
                messages.warning(request, 'Something went wrong. Please check form errors')
                return redirect('create-complaint')
    else:
        form = CreateComplaintForm()
        context = {'form': form}
        return render(request, 'complaint/create_complaint.html', context)
        
            

# cx can see all active complaints
def customer_active_complaints(request):
    context = {'complaints': Complaint.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')}
    
    return render(request, 'complaint/customer_active_complaints.html', context)


# cx can see all resolved complaints
def customer_resolved_complaints(request):
    complaints = Complaint.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')
    context = {'complaints':complaints}
    return render(request, 'complaint/customer_resolved_complaints.html', context)


# officer can see all his/her active complaints
def officer_active_complaints(request):
    complaints = Complaint.objects.filter(officer=request.user, is_resolved=False).order_by('-created_on')
    context = {'complaints':complaints}
    return render(request, 'complaint/officer_active_complaints.html', context)


# officer can see all his/her resolved complaints
def officer_resolved_complaints(request):
    complaints = Complaint.objects.filter(officer=request.user, is_resolved=True).order_by('-created_on')
    context = {'complaints':complaints}
    return render(request, 'complaint/officer_resolved_complaints.html', context)



from django.contrib import messages

# assign complaints to officers
def assign_complaint(request, complaint_id):
    complaint = Complaint.objects.get(complaint_id=complaint_id)
    if request.method == 'POST':
        form = AssignComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_officer = True
            var.status = 'Active'
            var.save()

            subject_admin = f'New complaint Submitted - #{var.complaint_id}'
            message_admin = f'A new complaint has been assigned to you. complaint ID: {var.complaint_id}'
            email_from_admin = 'kbobroberts@gmail.com'  # Replace with your email
            recipient_list_admin = ['kotakirobert7@gmail.com']  # Replace with the actual admin email
            send_mail(subject_admin, message_admin, email_from_admin, recipient_list_admin)
            
            messages.success(request, f'complaint has been assigned to {var.officer}')
            return redirect('complaint-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-complaint')  # check this out later
    else:
        form = AssignComplaintForm(instance=complaint)
        form.fields['officer'].queryset = User.objects.filter(is_officer=True)
        context = {'form': form, 'complaint': complaint}
        return render(request, 'complaint/assign_complaint.html', context)

        

# complaint details
def complaint_details(request, complaint_id):
    complaint = Complaint.objects.get(complaint_id=complaint_id)
    context = {'complaint':complaint}
    return render(request, 'complaint/complaint_details.html', context)


# complaint queue (for only admins)
def complaint_queue(request):
    complaints = Complaint.objects.filter(is_assigned_to_officer=False)
    context = {'complaints':complaints}
    return render(request, 'complaint/complaint_queue.html', context)


def resolve_complaint(request, complaint_id):
    complaint = Complaint.objects.get(complaint_id=complaint_id)
    if request.method == 'POST':
        rs = request.POST.get('rs')
        complaint.resolution_steps = rs 
        complaint.is_resolved = True
        complaint.status = 'Resolved'
        complaint.save()
        messages.success(request, 'complaint is now resolved and closed')
        return redirect('dashboard')