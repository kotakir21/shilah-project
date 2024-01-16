from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ticket.models import Ticket
from complaint.models import Complaint

@login_required
def dashboard(request):
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
            'tickets': tickets, 'active_tickets': active_tickets, 'closed_tickets': closed_tickets,
            'complaints': complaints, 'active_complaints': active_complaints, 'closed_complaints': closed_complaints,
        }

        return render(request, 'dashboard/customer_dashboard.html', context)
    elif request.user.is_engineer:
        # Tickets for engineer
        tickets = Ticket.objects.filter(engineer=request.user).count()
        active_tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).count()
        closed_tickets = Ticket.objects.filter(engineer=request.user, is_resolved=True).count()

        # Complaints for engineer
        complaints = Complaint.objects.filter(engineer=request.user).count()
        active_complaints = Complaint.objects.filter(engineer=request.user, is_resolved=False).count()
        closed_complaints = Complaint.objects.filter(engineer=request.user, is_resolved=True).count()

        context = {
            'tickets': tickets, 'active_tickets': active_tickets, 'closed_tickets': closed_tickets,
            'complaints': complaints, 'active_complaints': active_complaints, 'closed_complaints': closed_complaints,
        }

        return render(request, 'dashboard/engineer_dashboard.html', context)
    elif request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')
