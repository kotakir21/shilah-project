import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateideationForm, AssignideationForm  # Update form imports
from .models import Ideation  # Update model import

User = get_user_model()

# cx can create a ideation from here 
def create_ideation(request):  # Rename the function
    if request.method == 'POST':
        form = CreateideationForm(request.POST)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ideation_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.ideation_id = id
                    var.save()
                    # send email func
                    subject = f'{var.ideation_title} #{var.ideation_id}'
                    message = 'Thank you for creating a ideation, we will address it soon.'  # Update email message
                    email_from = 'cshilahkyatuhire@email.com'
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Your ideation has been submitted. We will address it soon.')  # Update success message
                    return redirect('customer-active-ideations')  # Update redirect
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-ideation')  # Update redirect
    else:
        form = CreateideationForm()  # Update form reference
        context = {'form': form}
        return render(request, 'ideation/create_ideation.html', context)  # Update template reference
            
# cx can see all active ideations
def customer_active_ideations(request):  # Rename the function
    ideations =     Ideation.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'ideations': ideations}  # Update context
    return render(request, 'ideation/customer_active_ideations.html', context)  # Update template reference

# cx can see all resolved ideations
def customer_resolved_ideations(request):  # Rename the function
    ideations = Ideation.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'ideations': ideations}  # Update context
    return render(request, 'ideation/customer_resolved_ideations.html', context)  # Update template reference

# officer can see all his/her active ideations
def officer_active_ideations(request):  # Rename the function
    ideations = Ideation.objects.filter(officer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'ideations': ideations}  # Update context
    return render(request, 'ideation/officer_active_ideations.html', context)  # Update template reference

# officer can see all his/her resolved ideations
def officer_resolved_ideations(request):  # Rename the function
    ideations = Ideation.objects.filter(officer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'ideations': ideations}  # Update context
    return render(request, 'ideation/officer_resolved_ideations.html', context)  # Update template reference

# assign ideations to officers
def assign_ideation(request, ideation_id):  # Rename the function
    ideation = Ideation.objects.get(ideation_id=ideation_id)  # Update model reference
    if request.method == 'POST':
        form = AssignideationForm(request.POST, instance=ideation)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_officer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'ideation has been assigned to {var.officer}')
            return redirect('ideation-queue')  # Update redirect
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ideation')  # Update redirect
    else:
        form = AssignideationForm(instance=ideation)  # Update form reference
        form.fields['officer'].queryset = User.objects.filter(is_officer=True)
        context = {'form': form, 'ideation': ideation}  # Update context
        return render(request, 'ideation/assign_ideation.html', context)  # Update template reference

# ideation details
def ideation_details(request, ideation_id):  # Rename the function
    ideation = Ideation.objects.get(ideation_id=ideation_id)  # Update model reference
    context = {'ideation': ideation}  # Update context
    return render(request, 'ideation/ideation_details.html', context)  # Update template reference

# ideation queue (for only admins)
def ideation_queue(request):  # Rename the function
    ideations = Ideation.objects.filter(is_assigned_to_officer=False)  # Update model reference
    context = {'ideations': ideations}  # Update context
    return render(request, 'ideation/ideation_queue.html', context)  # Update template reference

def resolve_ideation(request, ideation_id):  # Rename the function
    ideation = Ideation.objects.get(ideation_id=ideation_id)  # Update model reference
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ideation.resolution_steps = rs 
        ideation.is_resolved = True
        ideation.status = 'Resolved'
        ideation.save()
        messages.success(request, 'ideation is now resolved and closed')
        return redirect('dashboard')  # Update redirect

