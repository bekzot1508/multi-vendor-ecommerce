import pytest
from django.urls import reverse

from apps.common.tests.factories import AdminFactory, SellerFactory, UserFactory


@pytest.mark.django_db
def test_backoffice_dashboard_allows_admin(client):
    admin = AdminFactory()
    client.force_login(admin)

    response = client.get(reverse("backoffice:dashboard"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_backoffice_dashboard_blocks_customer(client):
    user = UserFactory()
    client.force_login(user)

    response = client.get(reverse("backoffice:dashboard"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_backoffice_dashboard_blocks_seller(client):
    seller = SellerFactory()
    client.force_login(seller)

    response = client.get(reverse("backoffice:dashboard"))

    assert response.status_code == 302