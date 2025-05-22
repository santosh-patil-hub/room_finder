from django.urls import path
from .views import owner_dashboard, tenant_dashboard

urlpatterns = [
    path('owner/dashboard/', owner_dashboard, name='owner_dashboard'),
    path('tenant/dashboard/', tenant_dashboard, name='tenant_dashboard'),
]
