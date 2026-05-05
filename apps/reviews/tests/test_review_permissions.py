import pytest

from apps.common.tests.factories import OrderFactory, OrderItemFactory, ProductFactory, UserFactory
from apps.reviews.models import Review


@pytest.mark.django_db
def test_user_can_create_review_for_own_delivered_item():
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
        comment="Great product",
    )

    assert review.user == user
    assert review.order_item == item


@pytest.mark.django_db
def test_other_user_should_not_own_reviewable_item_data():
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