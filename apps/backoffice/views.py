from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.shops.models import Shop
from apps.users.models import SellerProfile
from apps.catalog.models import Brand, Category
from apps.promotions.models import Coupon
from apps.shipping.models import ShippingMethod
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payouts.models import SellerPayout
from apps.catalog.models import Product
from apps.users.models import User

from apps.common.utils import paginate_queryset
from .mixins import BackofficeAccessMixin
from .forms import BrandForm, CategoryForm, CouponForm, ShippingMethodForm
from apps.notifications.models import EmailLog, Notification

from .selectors import (
    get_all_brands,
    get_all_categories,
    get_all_coupons,
    get_all_email_logs,
    get_all_notifications,
    get_all_orders,
    get_all_payments,
    get_all_payouts,
    get_all_products,
    get_all_shops,
    get_all_shipping_methods,
    get_all_users,
    get_backoffice_dashboard_metrics,
    get_low_stock_inventory,
    get_pending_seller_profiles,
)
from .services import (
    activate_product,
    activate_user,
    approve_seller_profile,
    approve_shop,
    block_shop,
    deactivate_product,
    deactivate_user,
    mark_payout_as_failed,
    mark_payout_as_paid,
    reject_seller_profile,
    reject_shop,
)




class BackofficeDashboardView(BackofficeAccessMixin, View):
    template_name = "backoffice/dashboard.html"

    def get(self, request):
        metrics = get_backoffice_dashboard_metrics()

        return render(
            request,
            self.template_name,
            {"metrics": metrics},
        )


#*************************************
#   to get pendding seller profiles
#*************************************
class SellerApprovalListView(BackofficeAccessMixin, View):

    template_name = "backoffice/seller_approvals.html"

    def get(self, request):

        profiles = get_pending_seller_profiles()

        return render(
            request,
            self.template_name,
            {"profiles": profiles},
        )


#*************************************
#   to approve pendding seller profiles
#*************************************
class ApproveSellerView(BackofficeAccessMixin, View):

    def post(self, request, profile_id):

        profile = get_object_or_404(SellerProfile, id=profile_id)

        approve_seller_profile(profile)

        return redirect("backoffice:seller_approvals")


#*************************************
#   to reject seller profiles
#*************************************
class RejectSellerView(BackofficeAccessMixin, View):

    def post(self, request, profile_id):

        profile = get_object_or_404(SellerProfile, id=profile_id)

        reject_seller_profile(profile)

        return redirect("backoffice:seller_approvals")


#*************************************
#   Shop List
#*************************************
class ShopListView(BackofficeAccessMixin, View):

    template_name = "backoffice/shops.html"

    def get(self, request):

        shops = get_all_shops()

        return render(
            request,
            self.template_name,
            {"shops": shops},
        )


#*************************************
#   to approve pendding Shop
#*************************************
class ApproveShopView(BackofficeAccessMixin, View):

    def post(self, request, shop_id):

        shop = get_object_or_404(Shop, id=shop_id)

        approve_shop(shop)

        return redirect("backoffice:shops")


#*************************************
#   to reject Shop
#*************************************
class RejectShopView(BackofficeAccessMixin, View):

    def post(self, request, shop_id):

        shop = get_object_or_404(Shop, id=shop_id)

        reject_shop(shop)

        return redirect("backoffice:shops")


#*************************************
#   to Block Shop
#*************************************
class BlockShopView(BackofficeAccessMixin, View):

    def post(self, request, shop_id):

        shop = get_object_or_404(Shop, id=shop_id)

        block_shop(shop)

        return redirect("backoffice:shops")

#****************************
#   Category List
#****************************
class CategoryListView(BackofficeAccessMixin, View):
    template_name = "backoffice/category_list.html"

    def get(self, request):
        categories = get_all_categories()
        return render(request, self.template_name, {"categories": categories})


#*************************************
#    Category Create
#*************************************
class CategoryCreateView(BackofficeAccessMixin, View):
    template_name = "backoffice/category_form.html"

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("backoffice:category_list")

        return render(request, self.template_name, {"form": form})


#*************************************
#   Category Update
#*************************************
class CategoryUpdateView(BackofficeAccessMixin, View):
    template_name = "backoffice/category_form.html"

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(
            request,
            self.template_name,
            {"form": form, "object": category},
        )

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect("backoffice:category_list")

        return render(
            request,
            self.template_name,
            {"form": form, "object": category},
        )

#***********************
#   Category Delete
#***********************
class CategoryDeleteView(BackofficeAccessMixin, View):
    template_name = "backoffice/category_confirm_delete.html"

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, self.template_name, {"object": category})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect("backoffice:category_list")


#************************
#   Brand List
#************************
class BrandListView(BackofficeAccessMixin, View):
    template_name = "backoffice/brand_list.html"

    def get(self, request):
        brands = get_all_brands()
        return render(request, self.template_name, {"brands": brands})


#*************************************
#   Brand Create
#*************************************
class BrandCreateView(BackofficeAccessMixin, View):
    template_name = "backoffice/brand_form.html"

    def get(self, request):
        form = BrandForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = BrandForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("backoffice:brand_list")

        return render(request, self.template_name, {"form": form})


#*************************************
#   Brand Update
#*************************************
class BrandUpdateView(BackofficeAccessMixin, View):
    template_name = "backoffice/brand_form.html"

    def get(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        form = BrandForm(instance=brand)
        return render(request, self.template_name, {"form": form, "object": brand})

    def post(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        form = BrandForm(request.POST, instance=brand)

        if form.is_valid():
            form.save()
            return redirect("backoffice:brand_list")

        return render(request, self.template_name, {"form": form, "object": brand})


#*************************************
#   Brand Delete
#*************************************
class BrandDeleteView(BackofficeAccessMixin, View):
    template_name = "backoffice/brand_confirm_delete.html"

    def get(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        return render(request, self.template_name, {"object": brand})

    def post(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        brand.delete()
        return redirect("backoffice:brand_list")


#*************************************
#   Shipping Method List
#*************************************
class ShippingMethodListView(BackofficeAccessMixin, View):
    template_name = "backoffice/shipping_method_list.html"

    def get(self, request):
        methods = get_all_shipping_methods()
        return render(request, self.template_name, {"methods": methods})


#*************************************
#   Shipping Method Create
#*************************************
class ShippingMethodCreateView(BackofficeAccessMixin, View):
    template_name = "backoffice/shipping_method_form.html"

    def get(self, request):
        form = ShippingMethodForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ShippingMethodForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("backoffice:shipping_method_list")

        return render(request, self.template_name, {"form": form})


#*************************************
#   Shipping Method Update
#*************************************
class ShippingMethodUpdateView(BackofficeAccessMixin, View):
    template_name = "backoffice/shipping_method_form.html"

    def get(self, request, pk):
        method = get_object_or_404(ShippingMethod, pk=pk)
        form = ShippingMethodForm(instance=method)
        return render(request, self.template_name, {"form": form, "object": method})

    def post(self, request, pk):
        method = get_object_or_404(ShippingMethod, pk=pk)
        form = ShippingMethodForm(request.POST, instance=method)

        if form.is_valid():
            form.save()
            return redirect("backoffice:shipping_method_list")

        return render(request, self.template_name, {"form": form, "object": method})


#*************************************
#   Shipping Method Delete
#*************************************
class ShippingMethodDeleteView(BackofficeAccessMixin, View):
    template_name = "backoffice/shipping_method_confirm_delete.html"

    def get(self, request, pk):
        method = get_object_or_404(ShippingMethod, pk=pk)
        return render(request, self.template_name, {"object": method})

    def post(self, request, pk):
        method = get_object_or_404(ShippingMethod, pk=pk)
        method.delete()
        return redirect("backoffice:shipping_method_list")


#*******************
#   Coupon List
#*******************
class CouponListView(BackofficeAccessMixin, View):
    template_name = "backoffice/coupon_list.html"

    def get(self, request):
        coupons = get_all_coupons()
        return render(request, self.template_name, {"coupons": coupons})


#*******************
#   Coupon Create
#*******************
class CouponCreateView(BackofficeAccessMixin, View):
    template_name = "backoffice/coupon_form.html"

    def get(self, request):
        form = CouponForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CouponForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("backoffice:coupon_list")

        return render(request, self.template_name, {"form": form})


#*******************
#   Coupon update
#*******************
class CouponUpdateView(BackofficeAccessMixin, View):
    template_name = "backoffice/coupon_form.html"

    def get(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        form = CouponForm(instance=coupon)
        return render(request, self.template_name, {"form": form, "object": coupon})

    def post(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        form = CouponForm(request.POST, instance=coupon)

        if form.is_valid():
            form.save()
            return redirect("backoffice:coupon_list")

        return render(request, self.template_name, {"form": form, "object": coupon})


#*******************
#   Coupon Delete
#*******************
class CouponDeleteView(BackofficeAccessMixin, View):
    template_name = "backoffice/coupon_confirm_delete.html"

    def get(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        return render(request, self.template_name, {"object": coupon})

    def post(self, request, pk):
        coupon = get_object_or_404(Coupon, pk=pk)
        coupon.delete()
        return redirect("backoffice:coupon_list")


#*******************
#   Order List
#*******************
class OrderListView(BackofficeAccessMixin, View):
    template_name = "backoffice/order_list.html"

    def get(self, request):
        search = request.GET.get("search")
        status = request.GET.get("status")

        orders = get_all_orders(
            search=search,
            status=status,
        )

        page_obj = paginate_queryset(request, orders, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "status": status,
            },
        )


#*******************
#   Order Detail
#*******************
class OrderDetailView(BackofficeAccessMixin, View):
    template_name = "backoffice/order_detail.html"

    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.select_related("user", "payment", "shipment")
            .prefetch_related("items", "status_history"),
            id=order_id,
        )
        return render(request, self.template_name, {"order": order})


#*******************
#   Payment List
#*******************
class PaymentListView(BackofficeAccessMixin, View):
    template_name = "backoffice/payment_list.html"

    def get(self, request):
        search = request.GET.get("search")
        status = request.GET.get("status")

        payments = get_all_payments(
            search=search,
            status=status,
        )

        page_obj = paginate_queryset(request, payments, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "status": status,
            },
        )


#*******************
#   Payment Detail
#*******************
class PaymentDetailView(BackofficeAccessMixin, View):
    template_name = "backoffice/payment_detail.html"

    def get(self, request, payment_id):
        payment = get_object_or_404(
            Payment.objects.select_related("order", "order__user")
            .prefetch_related("transactions", "callback_logs"),
            id=payment_id,
        )
        return render(request, self.template_name, {"payment": payment})


#*******************
#   Payout List
#*******************
class PayoutListView(BackofficeAccessMixin, View):
    template_name = "backoffice/payout_list.html"

    def get(self, request):
        search = request.GET.get("search")
        status = request.GET.get("status")

        payouts = get_all_payouts(
            search=search,
            status=status,
        )

        page_obj = paginate_queryset(request, payouts, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "status": status,
            },
        )


#***********************
#   Payout Mark Paid
#***********************
class PayoutMarkPaidView(BackofficeAccessMixin, View):
    def post(self, request, payout_id):
        payout = get_object_or_404(SellerPayout, id=payout_id)
        mark_payout_as_paid(payout)
        return redirect("backoffice:payout_list")


#***********************
#   Payout Mark Failed
#***********************
class PayoutMarkFailedView(BackofficeAccessMixin, View):
    def post(self, request, payout_id):
        payout = get_object_or_404(SellerPayout, id=payout_id)
        mark_payout_as_failed(payout)
        return redirect("backoffice:payout_list")


#***********************
#   Low Stock List
#***********************
class LowStockListView(BackofficeAccessMixin, View):
    template_name = "backoffice/low_stock_list.html"

    def get(self, request):
        items = get_low_stock_inventory()
        return render(request, self.template_name, {"items": items})


#***********************
#   User List
#***********************
class UserListView(BackofficeAccessMixin, View):
    template_name = "backoffice/user_list.html"

    def get(self, request):
        search = request.GET.get("search")
        role = request.GET.get("role")
        is_active = request.GET.get("is_active")

        users = get_all_users(
            search=search,
            role=role,
            is_active=is_active,
        )

        page_obj = paginate_queryset(request, users, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "role": role,
                "is_active": is_active,
            },
        )

#***********************
#   User Detail
#***********************
class UserDetailView(BackofficeAccessMixin, View):
    template_name = "backoffice/user_detail.html"

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {"object": user})

#***********************
#   User Activate
#***********************
class UserActivateView(BackofficeAccessMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        activate_user(user)
        return redirect("backoffice:user_list")


#***********************
#   User DeActivate
#***********************
class UserDeactivateView(BackofficeAccessMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        deactivate_user(user)
        return redirect("backoffice:user_list")


#***********************
#   Product List
#***********************
class ProductListView(BackofficeAccessMixin, View):
    template_name = "backoffice/product_list.html"

    def get(self, request):
        search = request.GET.get("search")
        is_active = request.GET.get("is_active")

        products = get_all_products(
            search=search,
            is_active=is_active,
        )

        page_obj = paginate_queryset(request, products, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "is_active": is_active,
            },
        )


#***********************
#   Product Detail
#***********************
class ProductDetailView(BackofficeAccessMixin, View):
    template_name = "backoffice/product_detail.html"

    def get(self, request, product_id):
        product = get_object_or_404(
            Product.objects.select_related("shop", "category", "brand")
            .prefetch_related("variants", "images"),
            id=product_id,
        )
        return render(request, self.template_name, {"object": product})


#***********************
#   Product Activate
#***********************
class ProductActivateView(BackofficeAccessMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        activate_product(product)
        return redirect("backoffice:product_list")


#***********************
#   Product DeActivate
#***********************
class ProductDeactivateView(BackofficeAccessMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        deactivate_product(product)
        return redirect("backoffice:product_list")


#***********************
#   Notification List
#***********************
class NotificationListView(BackofficeAccessMixin, View):
    template_name = "backoffice/notification_list.html"

    def get(self, request):
        search = request.GET.get("search")
        type_ = request.GET.get("type")
        is_read = request.GET.get("is_read")

        notifications = get_all_notifications(
            search=search,
            type_=type_,
            is_read=is_read,
        )

        page_obj = paginate_queryset(request, notifications, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "type": type_,
                "is_read": is_read,
            },
        )


#*************************
#   Notification Detail
#*************************
class NotificationDetailView(BackofficeAccessMixin, View):
    template_name = "backoffice/notification_detail.html"

    def get(self, request, notification_id):
        notification = get_object_or_404(
            Notification.objects.select_related("user"),
            id=notification_id,
        )

        return render(
            request,
            self.template_name,
            {"object": notification},
        )


#***********************
#   Email Log List
#***********************
class EmailLogListView(BackofficeAccessMixin, View):
    template_name = "backoffice/email_log_list.html"

    def get(self, request):
        search = request.GET.get("search")
        status = request.GET.get("status")

        email_logs = get_all_email_logs(
            search=search,
            status=status,
        )

        page_obj = paginate_queryset(request, email_logs, per_page=12)

        return render(
            request,
            self.template_name,
            {
                "page_obj": page_obj,
                "search": search,
                "status": status,
            },
        )

#***********************
#   Email Log Detail
#***********************
class EmailLogDetailView(BackofficeAccessMixin, View):
    template_name = "backoffice/email_log_detail.html"

    def get(self, request, email_log_id):
        email_log = get_object_or_404(EmailLog, id=email_log_id)

        return render(
            request,
            self.template_name,
            {"object": email_log},
        )