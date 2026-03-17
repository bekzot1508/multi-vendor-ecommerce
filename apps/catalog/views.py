from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import Product


#****************************
#   Product detail view
#****************************
class ProductDetailView(View):
    template_name = "catalog/product_detail.html"

    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects.select_related("shop", "category", "brand")
            .prefetch_related("images", "variants"),
            slug=slug,
            is_active=True,
        )

        return render(
            request,
            self.template_name,
            {"product": product},
        )