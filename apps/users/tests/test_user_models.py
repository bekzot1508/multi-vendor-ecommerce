import pytest

from apps.users.models import CustomerProfile, SellerProfile, User, UserRole


@pytest.mark.django_db
def test_customer_profile_is_created_automatically():
    user = User.objects.create_user(
        username="customer1",
        email="customer1@example.com",
        password="pass1234",
        full_name="Customer One",
        role=UserRole.CUSTOMER,
    )

    assert CustomerProfile.objects.filter(user=user).exists()
    assert not SellerProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_seller_profile_is_created_automatically():
    user = User.objects.create_user(
        username="seller1",
        email="seller1@example.com",
        password="pass1234",
        full_name="Seller One",
        role=UserRole.SELLER,
    )

    assert SellerProfile.objects.filter(user=user).exists()
    assert not CustomerProfile.objects.filter(user=user).exists()