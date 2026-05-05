import pytest
from unittest.mock import patch

from apps.notifications.models import EmailLog
from apps.notifications.services import send_email_with_log


@pytest.mark.django_db
@patch("apps.notifications.services.send_mail")
def test_send_email_with_log_marks_sent(mock_send_mail):
    mock_send_mail.return_value = 1

    send_email_with_log(
        to_email="user@test.com",
        subject="Hello",
        body="Body text",
    )

    email_log = EmailLog.objects.get(to_email="user@test.com")

    assert email_log.status == EmailLog.Status.SENT
    assert email_log.subject == "Hello"


@pytest.mark.django_db
@patch("apps.notifications.services.send_mail")
def test_send_email_with_log_marks_failed(mock_send_mail):
    mock_send_mail.side_effect = Exception("SMTP error")

    send_email_with_log(
        to_email="user@test.com",
        subject="Hello",
        body="Body text",
    )

    email_log = EmailLog.objects.get(to_email="user@test.com")

    assert email_log.status == EmailLog.Status.FAILED
    assert "SMTP error" in email_log.error_message