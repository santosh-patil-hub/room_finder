from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def owner_dashboard(request):
    if request.user.user_type != 'owner':
        return redirect('tenant_dashboard')
    return render(request, 'room/owner_dashboard.html')

@login_required
def tenant_dashboard(request):
    if request.user.user_type != 'tenant':
        return redirect('owner_dashboard')
    return render(request, 'room/tenant_dashboard.html')
