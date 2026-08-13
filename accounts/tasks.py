from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()

def _send_email(self, subject, message, user):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_activation_email_task(self, user_id, activation_link):

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    subject = "Confirmez votre adresse Email"
    message = render_to_string("accounts/emails/activation_email.txt", {"username" : user.username, "activation_link": activation_link})

    _send_email(self, subject, message, user)

    

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, user_id, reset_link):

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    subject = "Reinitialistion de ton mot de passe"
    message = render_to_string("accounts/emails/password_reset_email.txt", {"username" : user.username, "reset_link" : reset_link})

    _send_email(self, subject, message, user)