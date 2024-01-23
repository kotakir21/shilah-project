from django.urls import path
from . import views

urlpatterns = [
    path('create-ideation/', views.create_ideation, name='create-ideation'),  # Updated view and URL
    path('customer-active-ideations/', views.customer_active_ideations, name='customer-active-ideations'),  # Updated view and URL
    path('customer-resolved-ideations/', views.customer_resolved_ideations, name='customer-resolved-ideations'),  # Updated view and URL
    path('assign-ideation/<str:ideation_id>/', views.assign_ideation, name='assign-ideation'),  # Updated view and URL
    path('ideation-details/<str:ideation_id>/', views.ideation_details, name='ideation-details'),  # Updated view and URL
    path('ideation-queue/', views.ideation_queue, name='ideation-queue'),  # Updated view and URL
    path('officer-active-ideations/', views.officer_active_ideations, name='officer-active-ideations'),  # Updated view and URL
    path('officer-resolved-ideations/', views.officer_resolved_ideations, name='officer-resolved-ideations'),  # Updated view and URL
    path('resolve-ideation/<str:ideation_id>/', views.resolve_ideation, name='resolve-ideation'),  # Updated view and URL
]
