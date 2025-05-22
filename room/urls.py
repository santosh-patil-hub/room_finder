from django.urls import path
from .views import (
    RoomCreateAPIView,
    RoomListAPIView,
    RoomDetailAPIView,
    RoomUpdateAPIView,
    RoomDeleteAPIView,
    OwnerDashboardAPIView, 
    TenantDashboardAPIView
)

urlpatterns = [
    path('owner/dashboard/', OwnerDashboardAPIView, name='owner_dashboard'),
    path('tenant/dashboard/', TenantDashboardAPIView, name='tenant_dashboard'),
    path('rooms/', RoomListAPIView.as_view(), name='room-list'),             # GET list all rooms
    path('rooms/create/', RoomCreateAPIView.as_view(), name='room-create'),   # POST create room (owner only)
    path('rooms/<slug:slug>/', RoomDetailAPIView.as_view(), name='room-detail'),  # GET room detail
    path('rooms/<slug:slug>/update/', RoomUpdateAPIView.as_view(), name='room-update'),  # PUT/PATCH update room (owner only)
    path('rooms/<slug:slug>/delete/', RoomDeleteAPIView.as_view(), name='room-delete'),  # DELETE room (owner only)
]
