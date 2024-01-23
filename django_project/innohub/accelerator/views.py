import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateacceleratorForm, AssignacceleratorForm  # Update form imports
from .models import Accelerator  # Update model import

User = get_user_model()

# cx can create a accelerator from here 
def create_accelerator(request):  # Rename the function
    if request.method == 'POST':
        form = CreateacceleratorForm(request.POST)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.accelerator_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.accelerator_id = id
                    var.save()
                    # send email func
                    subject = f'{var.accelerator_title} #{var.accelerator_id}'
                    message = 'Thank you for creating a accelerator, we will address it soon.'  # Update email message
                    email_from = 'cshilahkyatuhire@email.com'
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Your accelerator has been submitted. We will address it soon.')  # Update success message
                    return redirect('customer-active-accelerators')  # Update redirect
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-accelerator')  # Update redirect
    else:
        form = CreateacceleratorForm()  # Update form reference
        context = {'form': form}
        return render(request, 'accelerator/create_accelerator.html', context)  # Update template reference
            
# cx can see all active accelerators
def customer_active_accelerators(request):  # Rename the function
    accelerators = Accelerator.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'accelerators': accelerators}  # Update context
    return render(request, 'accelerator/customer_active_accelerators.html', context)  # Update template reference

# cx can see all resolved accelerators
def customer_resolved_accelerators(request):  # Rename the function
    accelerators = Accelerator.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'accelerators': accelerators}  # Update context
    return render(request, 'accelerator/customer_resolved_accelerators.html', context)  # Update template reference

# officer can see all his/her active accelerators
def officer_active_accelerators(request):  # Rename the function
    accelerators = Accelerator.objects.filter(officer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'accelerators': accelerators}  # Update context
    return render(request, 'accelerator/officer_active_accelerators.html', context)  # Update template reference

# officer can see all his/her resolved accelerators
def officer_resolved_accelerators(request):  # Rename the function
    accelerators = Accelerator.objects.filter(officer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'accelerators': accelerators}  # Update context
    return render(request, 'accelerator/officer_resolved_accelerators.html', context)  # Update template reference

# assign accelerators to officers
def assign_accelerator(request, accelerator_id):  # Rename the function
    accelerator = Accelerator.objects.get(accelerator_id=accelerator_id)  # Update model reference
    if request.method == 'POST':
        form = AssignacceleratorForm(request.POST, instance=accelerator)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_officer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'accelerator has been assigned to {var.officer}')
            return redirect('accelerator-queue')  # Update redirect
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-accelerator')  # Update redirect
    else:
        form = AssignacceleratorForm(instance=accelerator)  # Update form reference
        form.fields['officer'].queryset = User.objects.filter(is_officer=True)
        context = {'form': form, 'accelerator': accelerator}  # Update context
        return render(request, 'accelerator/assign_accelerator.html', context)  # Update template reference

# accelerator details
def accelerator_details(request, accelerator_id):  # Rename the function
    accelerator = Accelerator.objects.get(accelerator_id=accelerator_id)  # Update model reference
    context = {'accelerator': accelerator}  # Update context
    return render(request, 'accelerator/accelerator_details.html', context)  # Update template reference

# accelerator queue (for only admins)
def accelerator_queue(request):  # Rename the function
    accelerators = Accelerator.objects.filter(is_assigned_to_officer=False)  # Update model reference
    context = {'accelerators': accelerators}  # Update context
    return render(request, 'accelerator/accelerator_queue.html', context)  # Update template reference

def resolve_accelerator(request, accelerator_id):  # Rename the function
    accelerator = Accelerator.objects.get(accelerator_id=accelerator_id)  # Update model reference
    if request.method == 'POST':
        rs = request.POST.get('rs')
        accelerator.resolution_steps = rs 
        accelerator.is_resolved = True
        accelerator.status = 'Resolved'
        accelerator.save()
        messages.success(request, 'accelerator is now resolved and closed')
        return redirect('dashboard')  # Update redirect

