from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_verification_email(user, request):
    from .tokens import email_verification_token
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    verification_link = f"http://{request.get_host()}/api/accounts/verify-email/{uid}/{token}/"

    subject = 'Verify Your Email'
    message = render_to_string('email_verification.html', {
        'user': user,
        'verification_link': verification_link
    })

    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)
