from django.urls import path
from . import views

urlpatterns = [
    path('create-accelerator/', views.create_accelerator, name='create-accelerator'),  # Updated view and URL
    path('customer-active-accelerators/', views.customer_active_accelerators, name='customer-active-accelerators'),  # Updated view and URL
    path('customer-resolved-accelerators/', views.customer_resolved_accelerators, name='customer-resolved-accelerators'),  # Updated view and URL
    path('assign-accelerator/<str:accelerator_id>/', views.assign_accelerator, name='assign-accelerator'),  # Updated view and URL
    path('accelerator-details/<str:accelerator_id>/', views.accelerator_details, name='accelerator-details'),  # Updated view and URL
    path('accelerator-queue/', views.accelerator_queue, name='accelerator-queue'),  # Updated view and URL
    path('officer-active-accelerators/', views.officer_active_accelerators, name='officer-active-accelerators'),  # Updated view and URL
    path('officer-resolved-accelerators/', views.officer_resolved_accelerators, name='officer-resolved-accelerators'),  # Updated view and URL
    path('resolve-accelerator/<str:accelerator_id>/', views.resolve_accelerator, name='resolve-accelerator'),  # Updated view and URL
]
