from django.conf import settings
from django.core.mail import send_mail


def contact_confirmation(email):
    message = 'Hey hey, whats up. Guess what, we received your email and will respond as fast as possible. If you need fast and short response consider contacting us on instagram at @sociale.x \nTake care, Sociale Team'
    send_mail(
        'Thanks for contacting us :)',
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
def contact_inbox(name,email,message):
    message = f'Name:{name}\nEmail:{email}\nMessage:\n{message}'
    send_mail(
        'Thanks for contacting us :)',
        message,
        settings.EMAIL_HOST_USER,
        ['inbox.sociale@gmail.com'],
        fail_silently=False
    )

def password_reset(email,uuid):
    message = f'Reset your password here: {settings.HOST}password-reset/{uuid}'
    send_mail(
        'Reset your Password',
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )