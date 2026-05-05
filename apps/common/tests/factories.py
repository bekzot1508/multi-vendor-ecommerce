import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.shops.models import Shop
from apps.catalog.models import Product, ProductVariant
from apps.inventory.models import InventoryRecord
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment
from apps.payouts.models import SellerPayout
from apps.shipping.models import Shipment
from apps.reviews.models import Review

User = get_user_model()


# ---------------- USERS ----------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.Sequence(lambda n: f"user{n}")
    full_name = factory.Faker("name")
    role = "customer"
    is_active = True


class SellerFactory(UserFactory):
    role = "seller"


class AdminFactory(UserFactory):
    role = "admin"
    is_staff = True


# ---------------- SHOP (OneToOne owner) ----------------
class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop

    owner = factory.SubFactory(SellerFactory)
    name = factory.Sequence(lambda n: f"Shop {n}")
    slug = factory.Sequence(lambda n: f"shop-{n}")
    status = "approved"


# 🔥 MUHIM: bitta seller uchun bitta shop reuse qilish helperi
def get_or_create_shop_for_seller(seller):
    shop, _ = Shop.objects.get_or_create(
        owner=seller,
        defaults={
            "name": f"{seller.username}-shop",
            "slug": f"{seller.username}-shop",
            "status": "approved",
        },
    )
    return shop


# ---------------- CATALOG ----------------
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    # default: yangi shop yaratadi
    shop = factory.SubFactory(ShopFactory)
    name = factory.Sequence(lambda n: f"Product {n}")
    slug = factory.Sequence(lambda n: f"product-{n}")
    is_active = True


class VariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    name = "Default"
    sku = factory.Sequence(lambda n: f"SKU{n}")
    price = 100
    is_active = True


# ---------------- INVENTORY ----------------
class InventoryRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryRecord

    variant = factory.SubFactory(VariantFactory)
    total_stock = 10
    reserved_stock = 0
    low_stock_threshold = 1


# ---------------- ORDERS ----------------
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    order_number = factory.Sequence(lambda n: f"ORD{n}")
    status = "pending"
    shipping_address_snapshot = "test"
    billing_address_snapshot = "test"

    # 🔥 MUHIM
    subtotal = 0
    discount_amount = 0
    shipping_amount = 0
    total_amount = 0


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    # default chain
    variant = factory.SubFactory(VariantFactory)

    # 🔥 zanjirni moslaymiz
    @factory.lazy_attribute
    def product(self):
        return self.variant.product

    @factory.lazy_attribute
    def shop(self):
        # product.shop bilan mos bo‘lsin
        return self.variant.product.shop

    order = factory.SubFactory(OrderFactory)

    quantity = 1
    unit_price = 100
    line_total = 100
    status = "processing"


# ---------------- PAYMENTS ----------------
class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    order = factory.SubFactory(OrderFactory)
    provider_name = "mock_gateway"
    external_reference = factory.Sequence(lambda n: f"PAY{n}")
    amount = 100
    status = "pending"


# ---------------- SHIPPING ----------------
class ShipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shipment

    order = factory.SubFactory(OrderFactory)
    status = "pending"
    tracking_code = factory.Sequence(lambda n: f"TRK{n}")


# ---------------- PAYOUTS ----------------
class PayoutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SellerPayout

    seller = factory.SubFactory(SellerFactory)
    amount = 100
    status = "pending"


# ---------------- REVIEWS ----------------
class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    order_item = factory.SubFactory(OrderItemFactory)

    rating = 5
    comment = factory.Faker("sentence")