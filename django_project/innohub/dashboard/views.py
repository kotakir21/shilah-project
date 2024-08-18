from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ticket.models import Ticket
from complaint.models import Complaint
from messaging.models import Message  # Import the Message model

@login_required
def dashboard(request):
    # Calculate unread message count
    unread_message_count = Message.objects.filter(receiver=request.user, is_read=False).count()

    if request.user.is_customer:
        # Tickets
        tickets = Ticket.objects.filter(customer=request.user).count()
        active_tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).count()
        closed_tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).count()

        # Complaints
        complaints = Complaint.objects.filter(customer=request.user).count()
        active_complaints = Complaint.objects.filter(customer=request.user, is_resolved=False).count()
        closed_complaints = Complaint.objects.filter(customer=request.user, is_resolved=True).count()

        context = {
            'tickets': tickets,
            'active_tickets': active_tickets,
            'closed_tickets': closed_tickets,
            'complaints': complaints,
            'active_complaints': active_complaints,
            'closed_complaints': closed_complaints,
            'unread_message_count': unread_message_count,  # Pass unread message count
        }

        return render(request, 'dashboard/customer_dashboard.html', context)

    elif request.user.is_officer:
        # Tickets for officer
        tickets = Ticket.objects.filter(officer=request.user).count()
        active_tickets = Ticket.objects.filter(officer=request.user, is_resolved=False).count()
        closed_tickets = Ticket.objects.filter(officer=request.user, is_resolved=True).count()

        # Complaints for officer
        complaints = Complaint.objects.filter(officer=request.user).count()
        active_complaints = Complaint.objects.filter(officer=request.user, is_resolved=False).count()
        closed_complaints = Complaint.objects.filter(officer=request.user, is_resolved=True).count()

        context = {
            'tickets': tickets,
            'active_tickets': active_tickets,
            'closed_tickets': closed_tickets,
            'complaints': complaints,
            'active_complaints': active_complaints,
            'closed_complaints': closed_complaints,
            'unread_message_count': unread_message_count,  # Pass unread message count
        }

        return render(request, 'dashboard/officer_dashboard.html', context)

    elif request.user.is_superuser:
        context = {
            'unread_message_count': unread_message_count,  # Pass unread message count for admin dashboard
        }
        return render(request, 'dashboard/admin_dashboard.html', context)
