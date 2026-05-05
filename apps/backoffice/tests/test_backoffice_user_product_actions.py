import pytest
from django.urls import reverse

from apps.common.tests.factories import AdminFactory, UserFactory, ProductFactory


@pytest.mark.django_db
def test_admin_can_deactivate_user(client):
    admin = AdminFactory()
    user = UserFactory(is_active=True)

    client.force_login(admin)

    response = client.post(
        reverse("backoffice:user_deactivate", kwargs={"user_id": user.id})
    )

    assert response.status_code == 302

    user.refresh_from_db()
    assert user.is_active is False


@pytest.mark.django_db
def test_admin_can_activate_user(client):
    admin = AdminFactory()
    user = UserFactory(is_active=False)

    client.force_login(admin)

    response = client.post(
        reverse("backoffice:user_activate", kwargs={"user_id": user.id})
    )

    assert response.status_code == 302

    user.refresh_from_db()
    assert user.is_active is True


@pytest.mark.django_db
def test_admin_can_deactivate_product(client):
    admin = AdminFactory()
    product = ProductFactory(is_active=True)

    client.force_login(admin)

    response = client.post(
        reverse("backoffice:product_deactivate", kwargs={"product_id": product.id})
    )

    assert response.status_code == 302

    product.refresh_from_db()
    assert product.is_active is False


@pytest.mark.django_db
def test_admin_can_activate_product(client):
    admin = AdminFactory()
    product = ProductFactory(is_active=False)

    client.force_login(admin)

    response = client.post(
        reverse("backoffice:product_activate", kwargs={"product_id": product.id})
    )

    assert response.status_code == 302

    product.refresh_from_db()
    assert product.is_active is True