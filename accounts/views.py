from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login
from rest_framework.authtoken.models import Token
from .utils import send_verification_email

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return Response({"message": "Check your email to verify account."}, status=201)
        return Response(serializer.errors, status=400)

class ActivateUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                token, _ = Token.objects.get_or_create(user=user)
                return Response({"message": "Account activated", "token": token.key})
            else:
                return Response({"error": "Invalid or expired link"}, status=400)

        except Exception:
            return Response({"error": "Activation failed"}, status=400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                return Response({"error": "Verify your email first"}, status=403)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_type": user.user_type})
        return Response({"error": "Invalid credentials"}, status=401)
