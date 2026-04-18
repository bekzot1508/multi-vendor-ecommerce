from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.shops.models import Shop, ShopStatus
from apps.users.models import UserRole
from apps.inventory.models import InventoryRecord
from .models import Product, ProductImage, ProductVariant

from .forms import ProductForm, ProductImageForm, ProductVariantForm
from apps.reviews.selectors import get_product_reviews
from .selectors import get_product_images_for_variant


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

        variant_id = request.GET.get("variant")

        selected_variant = None
        images = product.images.filter(variant__isnull=True)

        if variant_id:
            selected_variant = product.variants.filter(id=variant_id).first()
            images = get_product_images_for_variant(product, selected_variant)

        reviews = get_product_reviews(product)

        return render(
            request,
            self.template_name,
            {
                "product": product,
                "variants": product.variants.all(),
                "selected_variant": selected_variant,
                "images": images,
                "reviews": reviews,
            }
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

        shop = Shop.objects.filter(owner=request.user).first()

        if not shop:
            messages.error(request, "You need to create a shop first.")
            return redirect("shops:create")

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
        elif request.user.shop.status != ShopStatus.APPROVED:
            messages.error(request, "Your Shop is not approved to create Product. wait for!")
            return redirect("catalog:seller_product_list")
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
        elif request.user.shop.status != ShopStatus.APPROVED:
            messages.error(request, f"Your Shop is {request.user.shop.status}")
            return redirect("catalog:seller_product_list")

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
        elif request.user.shop.status != ShopStatus.APPROVED:
            messages.error(request, f"Your Shop is {request.user.shop.status}.")
            return redirect("catalog:seller_product_list")

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


#*******************************
#  Seller Product Manage view
#*******************************
class SellerProductManageView(LoginRequiredMixin, View):
    template_name = "catalog/seller_product_manage.html"

    def get(self, request, pk):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can manage products.")
            return redirect("users:profile")
        elif request.user.shop.status != ShopStatus.APPROVED:
            messages.error(request, f"Your Shop is {request.user.shop.status}")
            return redirect("catalog:seller_product_list")

        shop = get_object_or_404(Shop, owner=request.user)

        product = get_object_or_404(
            Product.objects.prefetch_related("variants", "images"),
            pk=pk,
            shop=shop,
        )

        variants = product.variants.all()
        images = product.images.all()

        return render(
            request,
            self.template_name,
            {
                "product": product,
                "variants": variants,
                "images": images,
            },
        )


#*******************************
#  Variant Create
#*******************************
class SellerVariantCreateView(LoginRequiredMixin, View):
    template_name = "catalog/variant_form.html"

    def get(self, request, product_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can create variants.")
            return redirect("users:profile")

        product = get_object_or_404(
            Product,
            id=product_id,
            shop__owner=request.user,
        )

        form = ProductVariantForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
            },
        )

    def post(self, request, product_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can create variants.")
            return redirect("users:profile")

        product = get_object_or_404(
            Product,
            id=product_id,
            shop__owner=request.user,
        )

        form = ProductVariantForm(request.POST)

        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = product
            variant.save()

            InventoryRecord.objects.get_or_create(variant=variant)

            messages.success(request, "Variant created successfully.")
            return redirect("catalog:seller_product_manage", pk=product.id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
            },
        )


#*******************************
#  Variant Update
#*******************************
class SellerVariantUpdateView(LoginRequiredMixin, View):
    template_name = "catalog/variant_form.html"

    def get(self, request, variant_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can update variants.")
            return redirect("users:profile")

        variant = get_object_or_404(
            ProductVariant.objects.select_related("product"),
            id=variant_id,
            product__shop__owner=request.user,
        )

        form = ProductVariantForm(instance=variant)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": variant.product,
                "variant": variant,
            },
        )

    def post(self, request, variant_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can update variants.")
            return redirect("users:profile")

        variant = get_object_or_404(
            ProductVariant.objects.select_related("product"),
            id=variant_id,
            product__shop__owner=request.user,
        )

        form = ProductVariantForm(request.POST, instance=variant)

        if form.is_valid():
            form.save()
            messages.success(request, "Variant updated successfully.")
            return redirect("catalog:seller_product_manage", pk=variant.product.id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": variant.product,
                "variant": variant,
            },
        )


#*******************************
#  Variant Delete
#*******************************
class SellerVariantDeleteView(LoginRequiredMixin, View):
    template_name = "catalog/variant_confirm_delete.html"

    def get(self, request, variant_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can delete variants.")
            return redirect("users:profile")

        variant = get_object_or_404(
            ProductVariant.objects.select_related("product"),
            id=variant_id,
            product__shop__owner=request.user,
        )

        return render(
            request,
            self.template_name,
            {
                "variant": variant,
                "product": variant.product,
            },
        )

    def post(self, request, variant_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can delete variants.")
            return redirect("users:profile")

        variant = get_object_or_404(
            ProductVariant.objects.select_related("product"),
            id=variant_id,
            product__shop__owner=request.user,
        )

        product_id = variant.product.id
        variant.delete()

        messages.success(request, "Variant deleted successfully.")
        return redirect("catalog:seller_product_manage", pk=product_id)


#*******************************
#  Image Create
#*******************************
class SellerImageCreateView(LoginRequiredMixin, View):
    template_name = "catalog/image_form.html"

    def get(self, request, product_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can upload images.")
            return redirect("users:profile")

        product = get_object_or_404(
            Product,
            id=product_id,
            shop__owner=request.user,
        )

        form = ProductImageForm(product=product)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
            },
        )

    def post(self, request, product_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can upload images.")
            return redirect("users:profile")

        product = get_object_or_404(
            Product,
            id=product_id,
            shop__owner=request.user,
        )

        form = ProductImageForm(request.POST, request.FILES)
        form = ProductImageForm(request.POST, request.FILES, product=product)

        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.save()

            messages.success(request, "Image uploaded successfully.")
            return redirect("catalog:seller_product_manage", pk=product.id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "product": product,
            },
        )


#*******************************
#  Image Delete
#*******************************
class SellerImageDeleteView(LoginRequiredMixin, View):
    template_name = "catalog/image_confirm_delete.html"

    def get(self, request, image_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can delete images.")
            return redirect("users:profile")

        image = get_object_or_404(
            ProductImage.objects.select_related("product"),
            id=image_id,
            product__shop__owner=request.user,
        )

        return render(
            request,
            self.template_name,
            {
                "image": image,
                "product": image.product,
            },
        )

    def post(self, request, image_id):
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can delete images.")
            return redirect("users:profile")

        image = get_object_or_404(
            ProductImage.objects.select_related("product"),
            id=image_id,
            product__shop__owner=request.user,
        )

        product_id = image.product.id
        image.delete()

        messages.success(request, "Image deleted successfully.")
        return redirect("catalog:seller_product_manage", pk=product_id)


class HomeView(View):
    template_name = "catalog/home.html"

    def get(self, request):
        products = (
            Product.objects
            .select_related("shop", "category", "brand")
            .prefetch_related("images")
            .filter(is_active=True)
            .order_by("-created_at")[:12]
        )

        return render(
            request,
            self.template_name,
            {"products": products},
        )


























