from config.celery import app
from django.conf import settings
from django.core.mail import send_mail


@app.task
def send_email(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
