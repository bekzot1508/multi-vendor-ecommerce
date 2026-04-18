from django.core.mail import send_mail
from django.conf import settings

from .models import EmailLog


def send_email_with_log(*, to_email, subject, body):

    email_log = EmailLog.objects.create(
        to_email=to_email,
        subject=subject,
        body=body,
        status=EmailLog.Status.PENDING,
    )

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )

        email_log.status = EmailLog.Status.SENT
        email_log.save(update_fields=["status"])

    except Exception as exc:

        email_log.status = EmailLog.Status.FAILED
        email_log.error_message = str(exc)

        email_log.save(update_fields=["status", "error_message"])