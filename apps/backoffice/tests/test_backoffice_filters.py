import pytest
from django.urls import reverse

from apps.common.tests.factories import AdminFactory, UserFactory


@pytest.mark.django_db
def test_admin_can_view_user_list(client):
    admin = AdminFactory()
    UserFactory()
    UserFactory()

    client.force_login(admin)

    response = client.get(reverse("backoffice:user_list"))

    assert response.status_code == 200