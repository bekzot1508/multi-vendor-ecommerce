import pytest

from apps.catalog.models import ProductImage
from apps.common.tests.factories import ProductFactory, VariantFactory


@pytest.mark.django_db
def test_product_can_have_multiple_variants():
    product = ProductFactory()

    v1 = VariantFactory(product=product, name="256GB Black")
    v2 = VariantFactory(product=product, name="512GB Gray")

    assert product.variants.count() == 2
    assert v1.product == product
    assert v2.product == product


@pytest.mark.django_db
def test_product_image_can_be_variant_specific():
    product = ProductFactory()
    variant = VariantFactory(product=product)

    image = ProductImage.objects.create(
        product=product,
        variant=variant,
        image="products/images/test.jpg",
        alt_text="Variant image",
        is_primary=True,
        sort_order=1,
    )

    assert image.product == product
    assert image.variant == variant


@pytest.mark.django_db
def test_product_image_can_be_product_level():
    product = ProductFactory()

    image = ProductImage.objects.create(
        product=product,
        variant=None,
        image="products/images/test2.jpg",
        alt_text="General product image",
        is_primary=False,
        sort_order=2,
    )

    assert image.product == product
    assert image.variant is None