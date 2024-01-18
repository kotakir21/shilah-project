import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateictsmeForm, AssignictsmeForm  # Update form imports
from .models import Ictsme  # Update model import

User = get_user_model()

# cx can create a ictsme from here 
def create_ictsme(request):  # Rename the function
    if request.method == 'POST':
        form = CreateictsmeForm(request.POST)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ictsme_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.ictsme_id = id
                    var.save()
                    # send email func
                    subject = f'{var.ictsme_title} #{var.ictsme_id}'
                    message = 'Thank you for creating a ictsme, we will address it soon.'  # Update email message
                    email_from = 'cshilahkyatuhire@email.com'
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Your ictsme has been submitted. We will address it soon.')  # Update success message
                    return redirect('customer-active-ictsmes')  # Update redirect
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-ictsme')  # Update redirect
    else:
        form = CreateictsmeForm()  # Update form reference
        context = {'form': form}
        return render(request, 'ictsme/create_ictsme.html', context)  # Update template reference
            
# cx can see all active ictsmes
def customer_active_ictsmes(request):  # Rename the function
    ictsmes = Ictsme.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'ictsmes': ictsmes}  # Update context
    return render(request, 'ictsme/customer_active_ictsmes.html', context)  # Update template reference

# cx can see all resolved ictsmes
def customer_resolved_ictsmes(request):  # Rename the function
    ictsmes = Ictsme.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'ictsmes': ictsmes}  # Update context
    return render(request, 'ictsme/customer_resolved_ictsmes.html', context)  # Update template reference

# engineer can see all his/her active ictsmes
def engineer_active_ictsmes(request):  # Rename the function
    ictsmes = Ictsme.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')  # Update model reference
    context = {'ictsmes': ictsmes}  # Update context
    return render(request, 'ictsme/engineer_active_ictsmes.html', context)  # Update template reference

# engineer can see all his/her resolved ictsmes
def engineer_resolved_ictsmes(request):  # Rename the function
    ictsmes = Ictsme.objects.filter(engineer=request.user, is_resolved=True).order_by('-created_on')  # Update model reference
    context = {'ictsmes': ictsmes}  # Update context
    return render(request, 'ictsme/engineer_resolved_ictsmes.html', context)  # Update template reference

# assign ictsmes to engineers
def assign_ictsme(request, ictsme_id):  # Rename the function
    ictsme = Ictsme.objects.get(ictsme_id=ictsme_id)  # Update model reference
    if request.method == 'POST':
        form = AssignictsmeForm(request.POST, instance=ictsme)  # Update form reference
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'ictsme has been assigned to {var.engineer}')
            return redirect('ictsme-queue')  # Update redirect
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ictsme')  # Update redirect
    else:
        form = AssignictsmeForm(instance=ictsme)  # Update form reference
        form.fields['engineer'].queryset = User.objects.filter(is_engineer=True)
        context = {'form': form, 'ictsme': ictsme}  # Update context
        return render(request, 'ictsme/assign_ictsme.html', context)  # Update template reference

# ictsme details
def ictsme_details(request, ictsme_id):  # Rename the function
    ictsme = Ictsme.objects.get(ictsme_id=ictsme_id)  # Update model reference
    context = {'ictsme': ictsme}  # Update context
    return render(request, 'ictsme/ictsme_details.html', context)  # Update template reference

# ictsme queue (for only admins)
def ictsme_queue(request):  # Rename the function
    ictsmes = Ictsme.objects.filter(is_assigned_to_engineer=False)  # Update model reference
    context = {'ictsmes': ictsmes}  # Update context
    return render(request, 'ictsme/ictsme_queue.html', context)  # Update template reference

def resolve_ictsme(request, ictsme_id):  # Rename the function
    ictsme = Ictsme.objects.get(ictsme_id=ictsme_id)  # Update model reference
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ictsme.resolution_steps = rs 
        ictsme.is_resolved = True
        ictsme.status = 'Resolved'
        ictsme.save()
        messages.success(request, 'ictsme is now resolved and closed')
        return redirect('dashboard')  # Update redirect

