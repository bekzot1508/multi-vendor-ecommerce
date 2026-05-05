import pytest
from django.db import IntegrityError

from apps.reviews.models import Review
from apps.common.tests.factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory


@pytest.mark.django_db
def test_review_belongs_to_same_user_as_order_item_owner():
    user = UserFactory()
    product = ProductFactory()
    order = OrderFactory(user=user, status="delivered")

    item = OrderItemFactory(
        order=order,
        product=product,
        variant__product=product,
        shop=product.shop,
        status="delivered",
    )

    review = Review.objects.create(
        user=user,
        product=product,
        order_item=item,
        rating=5,
        comment="Excellent",
    )

    assert review.user == item.order.user


@pytest.mark.django_db
def test_other_user_does_not_own_order_item_for_review():
    buyer = UserFactory()
    other_user = UserFactory()
    product = ProductFactory()
    order = OrderFactory(user=buyer, status="delivered")

    item = OrderItemFactory(
        order=order,
        product=product,
        variant__product=product,
        shop=product.shop,
        status="delivered",
    )

    assert item.order.user != other_user