from django.db import models
from django.db.models import Sum
from django.utils import timezone

from apps.inventory.models import InventoryRecord
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payouts.models import SellerPayout
from apps.shops.models import Shop, ShopStatus
from apps.users.models import SellerProfile, User, UserRole
from apps.catalog.models import Brand, Category
from apps.promotions.models import Coupon
from apps.shipping.models import ShippingMethod
from apps.catalog.models import Product
from apps.notifications.models import EmailLog, Notification





def get_backoffice_dashboard_metrics():
    today = timezone.now().date()

    total_users = User.objects.count()
    total_customers = User.objects.filter(role=UserRole.CUSTOMER).count()
    total_sellers = User.objects.filter(role=UserRole.SELLER).count()

    pending_seller_profiles = SellerProfile.objects.filter(is_approved=False).count()
    total_shops = Shop.objects.count()
    pending_shops = Shop.objects.filter(status=ShopStatus.PENDING).count()

    paid_orders = Order.objects.filter(status=Order.Status.PAID).count()
    payment_failed_orders = Order.objects.filter(status=Order.Status.PAYMENT_FAILED).count()

    today_revenue = (
        Order.objects.filter(
            status=Order.Status.PAID,
            paid_at__date=today,
        ).aggregate(total=Sum("total_amount"))["total"]
        or 0
    )

    low_stock_count = InventoryRecord.objects.filter(
        total_stock__lte=5
    ).count()

    pending_payouts = SellerPayout.objects.filter(
        status=SellerPayout.Status.PENDING
    ).count()

    successful_payments = Payment.objects.filter(
        status=Payment.Status.SUCCESS
    ).count()

    failed_payments = Payment.objects.filter(
        status=Payment.Status.FAILED
    ).count()

    return {
        "total_users": total_users,
        "total_customers": total_customers,
        "total_sellers": total_sellers,
        "pending_seller_profiles": pending_seller_profiles,
        "total_shops": total_shops,
        "pending_shops": pending_shops,
        "paid_orders": paid_orders,
        "payment_failed_orders": payment_failed_orders,
        "today_revenue": today_revenue,
        "low_stock_count": low_stock_count,
        "pending_payouts": pending_payouts,
        "successful_payments": successful_payments,
        "failed_payments": failed_payments,
    }


def get_pending_seller_profiles():
    return (
        SellerProfile.objects
        .select_related("user")
        .filter(is_approved=False)
        .order_by("-created_at")
    )


def get_all_shops():
    return (
        Shop.objects
        .select_related("owner")
        .order_by("-created_at")
    )


def get_all_categories():
    return Category.objects.select_related("parent").order_by("name")


def get_all_brands():
    return Brand.objects.order_by("name")


def get_all_shipping_methods():
    return ShippingMethod.objects.order_by("price", "name")


def get_all_coupons():
    return Coupon.objects.order_by("-created_at")


def get_all_orders(*, search=None, status=None):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("items", "status_history")
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            models.Q(order_number__icontains=search)
            | models.Q(user__email__icontains=search)
            | models.Q(user__full_name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    return queryset


def get_all_payments(*, search=None, status=None):
    queryset = (
        Payment.objects
        .select_related("order", "order__user")
        .prefetch_related("transactions", "callback_logs")
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            models.Q(external_reference__icontains=search)
            | models.Q(order__order_number__icontains=search)
            | models.Q(order__user__email__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    return queryset


def get_all_payouts(*, search=None, status=None):
    queryset = (
        SellerPayout.objects
        .select_related("seller")
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            models.Q(seller__email__icontains=search)
            | models.Q(seller__full_name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    return queryset


def get_low_stock_inventory():
    return (
        InventoryRecord.objects
        .select_related("variant", "variant__product", "variant__product__shop")
        .filter(total_stock__lte=5)
        .order_by("total_stock", "id")
    )


def get_all_users(*, search=None, role=None, is_active=None):
    queryset = User.objects.all().order_by("-created_at")

    if search:
        queryset = queryset.filter(
            models.Q(full_name__icontains=search)
            | models.Q(email__icontains=search)
            | models.Q(username__icontains=search)
        )

    if role:
        queryset = queryset.filter(role=role)

    if is_active in ["true", "false"]:
        queryset = queryset.filter(is_active=(is_active == "true"))

    return queryset


def get_all_products(*, search=None, is_active=None, shop_id=None):
    queryset = (
        Product.objects
        .select_related("shop", "category", "brand")
        .prefetch_related("variants", "images")
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            models.Q(name__icontains=search)
            | models.Q(slug__icontains=search)
            | models.Q(shop__name__icontains=search)
        )

    if is_active in ["true", "false"]:
        queryset = queryset.filter(is_active=(is_active == "true"))

    if shop_id:
        queryset = queryset.filter(shop_id=shop_id)

    return queryset


def get_all_notifications(*, search=None, type_=None, is_read=None):
    queryset = (
        Notification.objects
        .select_related("user")
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            models.Q(user__email__icontains=search)
            | models.Q(user__full_name__icontains=search)
            | models.Q(title__icontains=search)
            | models.Q(message__icontains=search)
        )

    if type_:
        queryset = queryset.filter(type=type_)

    if is_read in ["true", "false"]:
        queryset = queryset.filter(is_read=(is_read == "true"))

    return queryset


def get_all_email_logs(*, search=None, status=None):
    queryset = EmailLog.objects.order_by("-created_at")

    if search:
        queryset = queryset.filter(
            models.Q(to_email__icontains=search)
            | models.Q(subject__icontains=search)
            | models.Q(body__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    return queryset







