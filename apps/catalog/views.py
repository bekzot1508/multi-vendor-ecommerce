from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.shops.models import Shop
from apps.users.models import UserRole

from .forms import ProductForm
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


#*******************************
#  Seller Product list view
#*******************************
class SellerProductListView(LoginRequiredMixin, View):
    template_name = "catalog/seller_product_list.html"

    def get(self, request):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can access product management.")
            return redirect("users:profile")

        shop = get_object_or_404(Shop, owner=request.user)
        products = Product.objects.filter(shop=shop).select_related("category", "brand")

        return render(
            request,
            self.template_name,
            {
                "shop": shop,
                "products": products,
            },
        )


#*******************************
#  Seller Product create view
#*******************************
class SellerProductCreateView(LoginRequiredMixin, View):
    template_name = "catalog/product_form.html"

    def get(self, request):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can create products.")
            return redirect("users:profile")

        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can create products.")
            return redirect("users:profile")

        shop = get_object_or_404(Shop, owner=request.user)
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.save()

            messages.success(request, "Product created successfully.")
            return redirect("catalog:seller_product_list")

        return render(request, self.template_name, {"form": form})


#*******************************
#  Seller Product update view
#*******************************
class SellerProductUpdateView(LoginRequiredMixin, View):
    template_name = "catalog/product_form.html"

    def get(self, request, pk):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can update products.")
            return redirect("users:profile")

        shop = get_object_or_404(Shop, owner=request.user)
        product = get_object_or_404(Product, pk=pk, shop=shop)
        form = ProductForm(instance=product)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
            },
        )

    def post(self, request, pk):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can update products.")
            return redirect("users:profile")

        shop = get_object_or_404(Shop, owner=request.user)
        product = get_object_or_404(Product, pk=pk, shop=shop)
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("catalog:seller_product_list")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
            },
        )


#*******************************
#  Seller Product delete view
#*******************************
class SellerProductDeleteView(LoginRequiredMixin, View):
    template_name = "catalog/product_confirm_delete.html"

    def get(self, request, pk):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can delete products.")
            return redirect("users:profile")

        shop = get_object_or_404(Shop, owner=request.user)
        product = get_object_or_404(Product, pk=pk, shop=shop)

        return render(
            request,
            self.template_name,
            {"product": product},
        )

    def post(self, request, pk):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can delete products.")
            return redirect("users:profile")

        shop = get_object_or_404(Shop, owner=request.user)
        product = get_object_or_404(Product, pk=pk, shop=shop)
        product.delete()

        messages.success(request, "Product deleted successfully.")
        return redirect("catalog:seller_product_list")