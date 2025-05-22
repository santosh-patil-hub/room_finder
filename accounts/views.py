from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import User
from .utils import send_verification_email
from .tokens import email_verification_token

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return Response({"message": "Check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)
            dashboard = "owner_dashboard" if user.user_type == "owner" else "tenant_dashboard"
            return Response({"message": "Email verified!", "redirect": dashboard})
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            redirect_url = "owner_dashboard" if user.user_type == "owner" else "tenant_dashboard"
            return Response({"message": "Login successful", "redirect": redirect_url})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
