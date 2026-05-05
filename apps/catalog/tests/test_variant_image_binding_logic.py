import pytest

from apps.catalog.models import ProductImage
from apps.common.tests.factories import ProductFactory, VariantFactory


@pytest.mark.django_db
def test_multiple_variant_specific_images_can_belong_to_same_product():
    product = ProductFactory()
    v1 = VariantFactory(product=product, name="256GB Black")
    v2 = VariantFactory(product=product, name="512GB Gray")

    img1 = ProductImage.objects.create(
        product=product,
        variant=v1,
        image="products/images/black1.jpg",
        alt_text="Black image 1",
        is_primary=True,
        sort_order=1,
    )

    img2 = ProductImage.objects.create(
        product=product,
        variant=v2,
        image="products/images/gray1.jpg",
        alt_text="Gray image 1",
        is_primary=True,
        sort_order=1,
    )

    assert img1.variant == v1
    assert img2.variant == v2
    assert img1.product == product
    assert img2.product == product


@pytest.mark.django_db
def test_product_can_have_general_and_variant_images_together():
    product = ProductFactory()
    variant = VariantFactory(product=product)

    general = ProductImage.objects.create(
        product=product,
        variant=None,
        image="products/images/general.jpg",
        alt_text="General",
        is_primary=False,
        sort_order=1,
    )

    specific = ProductImage.objects.create(
        product=product,
        variant=variant,
        image="products/images/specific.jpg",
        alt_text="Specific",
        is_primary=True,
        sort_order=2,
    )

    assert general.variant is None
    assert specific.variant == variant
    assert product.images.count() == 2