import pytest
from django.urls import reverse

from apps.users.models import Address
from apps.common.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_cannot_edit_another_users_address(client):
    user1 = UserFactory()
    user2 = UserFactory()

    address = Address.objects.create(
        user=user1,
        full_name="User One",
        phone="123",
        country="UZ",
        city="Tashkent",
        area="A",
        line1="Line1",
        postal_code="1000",
    )

    client.force_login(user2)

    response = client.get(
        reverse("users:address_edit", kwargs={"pk": address.pk})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_delete_another_users_address(client):
    user1 = UserFactory()
    user2 = UserFactory()

    address = Address.objects.create(
        user=user1,
        full_name="User One",
        phone="123",
        country="UZ",
        city="Tashkent",
        area="A",
        line1="Line1",
        postal_code="1000",
    )

    client.force_login(user2)

    response = client.post(
        reverse("users:address_delete", kwargs={"pk": address.pk})
    )

    assert response.status_code == 404