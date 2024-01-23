import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateTicketForm, AssignTicketForm
from .models import Ticket

User = get_user_model()

# cx can create a ticket from here 
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.ticket_id = id
                    var.save()

                    # Send email to customer
                    subject_customer = f'Ticket Submitted Successfully - #{var.ticket_id}'
                    message_customer = 'Thank you for creating a ticket. A Support officer will be assigned soon.'
                    email_from_customer = 'your-email@example.com'  # Replace with your email
                    recipient_list_customer = [request.user.email]
                    send_mail(subject_customer, message_customer, email_from_customer, recipient_list_customer)

                    # Send email to admin
                    subject_admin = f'New Ticket Submitted - #{var.ticket_id}'
                    message_admin = f'A new ticket has been submitted by {request.user.email}. Ticket ID: {var.ticket_id}'
                    email_from_admin = 'kbobroberts@gmail.com'  # Replace with your email
                    recipient_list_admin = ['kotakirobert7@gmail.com']  # Replace with the actual admin email
                    send_mail(subject_admin, message_admin, email_from_admin, recipient_list_admin)

                    messages.success(request, 'Your ticket has been submitted. A Support officer will be assigned soon.')
                    return redirect('customer-active-tickets')

                except IntegrityError:
                    continue

            else:
                messages.warning(request, 'Something went wrong. Please check form errors')
                return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)
        
            

# cx can see all active tickets
def customer_active_tickets(request):
    context = {'tickets': Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')}
    
    return render(request, 'ticket/customer_active_tickets.html', context)


# cx can see all resolved tickets
def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/customer_resolved_tickets.html', context)


# officer can see all his/her active tickets
def officer_active_tickets(request):
    tickets = Ticket.objects.filter(officer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/officer_active_tickets.html', context)


# officer can see all his/her resolved tickets
def officer_resolved_tickets(request):
    tickets = Ticket.objects.filter(officer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/officer_resolved_tickets.html', context)



from django.contrib import messages

# assign tickets to officers
def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_officer = True
            var.status = 'Active'
            var.save()

            subject_admin = f'New Ticket Submitted - #{var.ticket_id}'
            message_admin = f'A new ticket has been assigned to you. Ticket ID: {var.ticket_id}'
            email_from_admin = 'kbobroberts@gmail.com'  # Replace with your email
            recipient_list_admin = ['kotakirobert7@gmail.com']  # Replace with the actual admin email
            send_mail(subject_admin, message_admin, email_from_admin, recipient_list_admin)
            
            messages.success(request, f'Ticket has been assigned to {var.officer}')
            return redirect('ticket-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ticket')  # check this out later
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['officer'].queryset = User.objects.filter(is_officer=True)
        context = {'form': form, 'ticket': ticket}
        return render(request, 'ticket/assign_ticket.html', context)

        

# ticket details
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket':ticket}
    return render(request, 'ticket/ticket_details.html', context)


# ticket queue (for only admins)
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_officer=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket_queue.html', context)


def resolve_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs 
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'Ticket is now resolved and closed')
        return redirect('dashboard')