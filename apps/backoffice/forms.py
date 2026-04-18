from django import forms

from apps.catalog.models import Brand, Category
from apps.promotions.models import Coupon
from apps.shipping.models import ShippingMethod


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "parent", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "slug": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "parent": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4",
            }),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ("name", "slug", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "slug": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4",
            }),
        }


class ShippingMethodForm(forms.ModelForm):
    class Meta:
        model = ShippingMethod
        fields = ("name", "price", "estimated_days", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "step": "0.01",
            }),
            "estimated_days": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4",
            }),
        }


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = (
            "code",
            "discount_type",
            "value",
            "min_order_amount",
            "max_discount_amount",
            "usage_limit",
            "per_user_limit",
            "starts_at",
            "ends_at",
            "is_active",
        )
        widgets = {
            "code": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "discount_type": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "value": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "step": "0.01",
            }),
            "min_order_amount": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "step": "0.01",
            }),
            "max_discount_amount": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "step": "0.01",
            }),
            "usage_limit": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "per_user_limit": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }),
            "starts_at": forms.DateTimeInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "type": "datetime-local",
            }),
            "ends_at": forms.DateTimeInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "type": "datetime-local",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4",
            }),
        }