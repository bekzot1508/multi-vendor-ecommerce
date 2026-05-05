import pytest
from django.urls import reverse

from apps.users.models import Address
from apps.common.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_can_create_address(client):
    user = UserFactory()
    client.force_login(user)

    response = client.post(
        reverse("users:address_create"),
        data={
            "full_name": "Test",
            "phone": "123",
            "country": "UZ",
            "city": "Tashkent",
            "area": "A",
            "line1": "Line1",
            "postal_code": "1000",
        },
    )

    assert response.status_code == 302
    assert Address.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_user_can_update_address(client):
    user = UserFactory()
    address = Address.objects.create(
        user=user,
        full_name="Old",
        phone="123",
        country="UZ",
        city="Tashkent",
        area="A",
        line1="Line1",
        postal_code="1000",
    )

    client.force_login(user)

    response = client.post(
        reverse("users:address_edit", kwargs={"pk": address.pk}),
        data={
            "full_name": "New",
            "phone": "999",
            "country": "UZ",
            "city": "Tashkent",
            "area": "B",
            "line1": "NewLine",
            "postal_code": "2000",
        },
    )

    assert response.status_code == 302

    address.refresh_from_db()
    assert address.full_name == "New"