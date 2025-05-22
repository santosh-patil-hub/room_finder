from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"http://localhost:8000/api/auth/activate/{uid}/{token}/"

    subject = "Activate your RoomFinder account"
    html_message = render_to_string("email/activation_email.html", {
        'user': user,
        'activation_link': link,
    })

    msg = EmailMultiAlternatives(subject, '', to=[user.email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
