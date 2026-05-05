import pytest

from apps.orders.models import Order
from apps.shipping.models import Shipment, ShippingMethod
from apps.shipping.services import update_shipment_status
from apps.common.tests.factories import AdminFactory, OrderFactory


@pytest.mark.django_db
def test_shipment_cannot_update_for_payment_failed_order():
    admin = AdminFactory()

    order = OrderFactory(status=Order.Status.PAYMENT_FAILED)
    shipping_method = ShippingMethod.objects.create(
        name="Standard",
        price=10,
        estimated_days=3,
        is_active=True,
    )
    shipment = Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code="TRK-FAIL-1",
        status=Shipment.Status.PENDING,
    )

    with pytest.raises(ValueError):
        update_shipment_status(
            shipment=shipment,
            changed_by=admin,
            new_status=Shipment.Status.IN_TRANSIT,
        )


@pytest.mark.django_db
def test_delivered_shipment_cannot_be_downgraded():
    admin = AdminFactory()

    order = OrderFactory(status=Order.Status.SHIPPED)
    shipping_method = ShippingMethod.objects.create(
        name="Express",
        price=20,
        estimated_days=1,
        is_active=True,
    )
    shipment = Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code="TRK-DELIV-1",
        status=Shipment.Status.DELIVERED,
    )

    with pytest.raises(ValueError):
        update_shipment_status(
            shipment=shipment,
            changed_by=admin,
            new_status=Shipment.Status.IN_TRANSIT,
        )