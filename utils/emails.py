from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings



def send_email(email, text_content, html_content):
    msg = EmailMultiAlternatives(
        'Verify your account',
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=False)

def send_verification_email(email: str, uid: str, token: str):
    verification_link: str = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}"
    text_content = render_to_string(
        'todo/my_email.txt',
        context={'verification_link': verification_link},
    )

    html_content = render_to_string(
        'todo/my_email.html',
        context={'verification_link': verification_link},
    )
    send_email(email, text_content, html_content)

def send_password_reset_email(email: str, uid: str, token: str):
    password_reset_link: str = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
    text_content = render_to_string(
        'todo/my_email.txt',
        context={'password_reset_link': password_reset_link},
    )

    html_content = render_to_string(
        'todo/my_email.html',
        context={'password_reset_link': password_reset_link},
    )
    send_email(email, text_content, html_content)