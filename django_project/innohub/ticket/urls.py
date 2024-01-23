from django.urls import path 
from . import views 

urlpatterns = [
    path('create-ticket/', views.create_ticket, name='create-ticket'), 
    path('customer-active-tickets/', views.customer_active_tickets, name='customer-active-tickets'),
    path('customer-resolved-tickets/', views.customer_resolved_tickets, name='customer-resolved-tickets'), 
    path('assign-ticket/<str:ticket_id>/', views.assign_ticket, name='assign-ticket'), 
    path('ticket-details/<str:ticket_id>/', views.ticket_details, name='ticket-details'), 
    path('ticket-queue/', views.ticket_queue, name='ticket-queue'), 
    path('officer-active-tickets/', views.officer_active_tickets, name='officer-active-tickets'), 
    path('officer-resolved-tickets/', views.officer_resolved_tickets, name='officer-resolved-tickets'), 
    path('resolve-ticket/<str:ticket_id>/', views.resolve_ticket, name='resolve-ticket')
]