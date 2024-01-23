from django.urls import path
from . import views

urlpatterns = [
    path('create-incubator/', views.create_incubator, name='create-incubator'),  # Updated view and URL
    path('customer-active-incubators/', views.customer_active_incubators, name='customer-active-incubators'),  # Updated view and URL
    path('customer-resolved-incubators/', views.customer_resolved_incubators, name='customer-resolved-incubators'),  # Updated view and URL
    path('assign-incubator/<str:incubator_id>/', views.assign_incubator, name='assign-incubator'),  # Updated view and URL
    path('incubator-details/<str:incubator_id>/', views.incubator_details, name='incubator-details'),  # Updated view and URL
    path('incubator-queue/', views.incubator_queue, name='incubator-queue'),  # Updated view and URL
    path('officer-active-incubators/', views.officer_active_incubators, name='officer-active-incubators'),  # Updated view and URL
    path('officer-resolved-incubators/', views.officer_resolved_incubators, name='officer-resolved-incubators'),  # Updated view and URL
    path('resolve-incubator/<str:incubator_id>/', views.resolve_incubator, name='resolve-incubator'),  # Updated view and URL
]
