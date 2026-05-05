import pytest

from apps.shipping.models import Shipment, ShippingMethod
from apps.shipping.services import update_shipment_status
from apps.common.tests.factories import AdminFactory, OrderFactory


@pytest.mark.django_db
def test_cannot_move_from_delivered_to_pending():
    admin = AdminFactory()
    order = OrderFactory()

    method = ShippingMethod.objects.create(
        name="Standard", price=10, estimated_days=3
    )

    shipment = Shipment.objects.create(
        order=order,
        shipping_method=method,
        tracking_code="TRK123",
        status=Shipment.Status.DELIVERED,
    )

    with pytest.raises(ValueError):
        update_shipment_status(
            shipment=shipment,
            changed_by=admin,
            new_status=Shipment.Status.PENDING,
        )