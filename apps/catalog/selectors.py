def get_product_images_for_variant(product, variant=None):
    """
    Priority:
    1. variant-specific images
    2. fallback → product images
    """

    if variant:
        variant_images = product.images.filter(variant=variant)

        if variant_images.exists():
            return variant_images

    return product.images.filter(variant__isnull=True)