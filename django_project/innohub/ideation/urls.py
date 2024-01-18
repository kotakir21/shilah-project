from django.urls import path
from . import views

urlpatterns = [
    path('create-ideation/', views.create_ideation, name='create-ideation'),  # Updated view and URL
    path('customer-active-ideations/', views.customer_active_ideations, name='customer-active-ideations'),  # Updated view and URL
    path('customer-resolved-ideations/', views.customer_resolved_ideations, name='customer-resolved-ideations'),  # Updated view and URL
    path('assign-ideation/<str:ideation_id>/', views.assign_ideation, name='assign-ideation'),  # Updated view and URL
    path('ideation-details/<str:ideation_id>/', views.ideation_details, name='ideation-details'),  # Updated view and URL
    path('ideation-queue/', views.ideation_queue, name='ideation-queue'),  # Updated view and URL
    path('engineer-active-ideations/', views.engineer_active_ideations, name='engineer-active-ideations'),  # Updated view and URL
    path('engineer-resolved-ideations/', views.engineer_resolved_ideations, name='engineer-resolved-ideations'),  # Updated view and URL
    path('resolve-ideation/<str:ideation_id>/', views.resolve_ideation, name='resolve-ideation'),  # Updated view and URL
]
