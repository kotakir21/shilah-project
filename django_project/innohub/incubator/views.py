import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateincubatorForm, AssignincubatorForm  # Update form imports
from .models import Incubator  # Update model import

User = get_user_model()

# cx can create a incubator from here 
def create_incubator(request):  # Rename the function
    if request.method == 'POST':
        form = CreateincubatorForm(request.POST)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.incubator_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.incubator_id = id
                    var.save()
                    # send email func
                    subject = f'{var.incubator_title} #{var.incubator_id}'
                    message = 'Thank you for creating a incubator, we will address it soon.'  # Update email message
                    email_from = 'cshilahkyatuhire@email.com'
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Your incubator has been submitted. We will address it soon.')  # Update success message
                    return redirect('customer-active-incubators')  # Update redirect
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-incubator')  # Update redirect
    else:
        form = CreateincubatorForm()  # Update form reference
        context = {'form': form}
        return render(request, 'incubator/create_incubator.html', context)  # Update template reference
            
# cx can see all active incubators
def customer_active_incubators(request):  # Rename the function
    incubators = Incubator.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'incubators': incubators}  # Update context
    return render(request, 'incubator/customer_active_incubators.html', context)  # Update template reference

# cx can see all resolved incubators
def customer_resolved_incubators(request):  # Rename the function
    incubators = Incubator.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'incubators': incubators}  # Update context
    return render(request, 'incubator/customer_resolved_incubators.html', context)  # Update template reference

# officer can see all his/her active incubators
def officer_active_incubators(request):  # Rename the function
    incubators = Incubator.objects.filter(officer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'incubators': incubators}  # Update context
    return render(request, 'incubator/officer_active_incubators.html', context)  # Update template reference

# officer can see all his/her resolved incubators
def officer_resolved_incubators(request):  # Rename the function
    incubators = incubator.objects.filter(officer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'incubators': incubators}  # Update context
    return render(request, 'incubator/officer_resolved_incubators.html', context)  # Update template reference

# assign incubators to officers
def assign_incubator(request, incubator_id):  # Rename the function
    incubator = Incubator.objects.get(incubator_id=incubator_id)  # Update model reference
    if request.method == 'POST':
        form = AssignincubatorForm(request.POST, instance=incubator)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_officer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'incubator has been assigned to {var.officer}')
            return redirect('incubator-queue')  # Update redirect
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-incubator')  # Update redirect
    else:
        form = AssignincubatorForm(instance=incubator)  # Update form reference
        form.fields['officer'].queryset = User.objects.filter(is_officer=True)
        context = {'form': form, 'incubator': incubator}  # Update context
        return render(request, 'incubator/assign_incubator.html', context)  # Update template reference

# incubator details
def incubator_details(request, incubator_id):  # Rename the function
    incubator = Incubator.objects.get(incubator_id=incubator_id)  # Update model reference
    context = {'incubator': incubator}  # Update context
    return render(request, 'incubator/incubator_details.html', context)  # Update template reference

# incubator queue (for only admins)
def incubator_queue(request):  # Rename the function
    incubators = Incubator.objects.filter(is_assigned_to_officer=False)  # Update model reference
    context = {'incubators': incubators}  # Update context
    return render(request, 'incubator/incubator_queue.html', context)  # Update template reference

def resolve_incubator(request, incubator_id):  # Rename the function
    incubator = Incubator.objects.get(incubator_id=incubator_id)  # Update model reference
    if request.method == 'POST':
        rs = request.POST.get('rs')
        incubator.resolution_steps = rs 
        incubator.is_resolved = True
        incubator.status = 'Resolved'
        incubator.save()
        messages.success(request, 'incubator is now resolved and closed')
        return redirect('dashboard')  # Update redirect

