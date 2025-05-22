from django.urls import path
from .views import RegisterView, ActivateUserView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
]
