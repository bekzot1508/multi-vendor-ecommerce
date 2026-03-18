from django.db import transaction

from apps.inventory.models import InventoryRecord

from .models import Cart, CartItem

#**************************
#   Get or create cart
#**************************
def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart



#**************************
#   Add item to cart
#**************************
@transaction.atomic
def add_item_to_cart(user, variant, quantity):
    cart = get_or_create_cart(user)

    if not variant.is_active:
        raise ValueError("Variant is inactive")

    inventory = InventoryRecord.objects.get(variant=variant)
    available = inventory.total_stock - inventory.reserved_stock

    if quantity > available:
        raise ValueError("Not enough stock")

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={
            "quantity": quantity,
            "unit_price": variant.price,
        },
    )

    if not created:
        new_qty = item.quantity + quantity

        if new_qty > available:
            raise ValueError("Not enough stock")

        item.quantity = new_qty
        item.save()

    return item


#**************************
#   Update quantity
#**************************
@transaction.atomic
def update_cart_item_quantity(user, item_id, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    cart = user.cart
    item = cart.items.select_related("variant").get(id=item_id)

    inventory = InventoryRecord.objects.get(variant=item.variant)
    available = inventory.total_stock - inventory.reserved_stock

    if quantity > available:
        raise ValueError("Not enough stock")

    item.quantity = quantity
    item.save()

    return item


#**************************
#   Remove item
#**************************
def remove_cart_item(user, item_id):
    cart = user.cart
    item = cart.items.get(id=item_id)
    item.delete()


#**********************
#   Cart total
#**********************
def calculate_cart_totals(cart):
    subtotal = sum(item.line_total() for item in cart.items.all())

    return {
        "subtotal": subtotal,
        "total": subtotal,  # coupon/shipping keyin qo‘shiladi
    }






