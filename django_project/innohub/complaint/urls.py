from django.urls import path
from . import views

urlpatterns = [
    path('create-complaint/', views.create_complaint, name='create-complaint'),  # Updated view and URL
    path('customer-active-complaints/', views.customer_active_complaints, name='customer-active-complaints'),  # Updated view and URL
    path('customer-resolved-complaints/', views.customer_resolved_complaints, name='customer-resolved-complaints'),  # Updated view and URL
    path('assign-complaint/<str:complaint_id>/', views.assign_complaint, name='assign-complaint'),  # Updated view and URL
    path('complaint-details/<str:complaint_id>/', views.complaint_details, name='complaint-details'),  # Updated view and URL
    path('complaint-queue/', views.complaint_queue, name='complaint-queue'),  # Updated view and URL
    path('officer-active-complaints/', views.officer_active_complaints, name='officer-active-complaints'),  # Updated view and URL
    path('officer-resolved-complaints/', views.officer_resolved_complaints, name='officer-resolved-complaints'),  # Updated view and URL
    path('resolve-complaint/<str:complaint_id>/', views.resolve_complaint, name='resolve-complaint'),  # Updated view and URL
]
