import pytest
from django.urls import reverse

from apps.users.models import UserRole, User
from apps.common.tests.factories import UserFactory


@pytest.mark.django_db
def test_register_cannot_create_admin_role(client):
    response = client.post(
        reverse("users:register"),
        data={
            "username": "eviladmin",
            "email": "evil@test.com",
            "full_name": "Evil Admin",
            "role": UserRole.ADMIN,
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 200
    assert User.objects.filter(username="eviladmin").count() == 0


@pytest.mark.django_db
def test_login_requires_valid_credentials(client):
    user = UserFactory(username="bekzot", email="bekzot@test.com")

    user.set_password("StrongPass123!")
    user.save(update_fields=["password"])

    response = client.post(
        reverse("users:login"),
        data={
            "username": "bekzot",
            "password": "wrongpass",
        },
    )

    assert response.status_code == 200
        # login form qaytadi, session ochilmaydi

    response = client.post(
        reverse("users:login"),
        data={
            "username": "bekzot",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 302