from django import forms

from .models import Product, ProductImage, ProductVariant


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category",
            "brand",
            "name",
            "description",
            "is_active",
        )

        # this is for style(UI)
        widgets = {
            "category": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
            }),
            "brand": forms.Select(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
            }),
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "placeholder": "Enter product name",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "rows": 5,
                "placeholder": "Write product description",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4"
            }),
        }


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = (
            "name",
            "sku",
            "price",
            "compare_at_price",
            "is_active",
        )

        # this is for style(UI)
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "placeholder": "e.g. Black / 256GB",
            }),
            "sku": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "placeholder": "Unique SKU",
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "step": "0.01",
            }),
            "compare_at_price": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "step": "0.01",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4"
            }),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["variant", "image", "alt_text", "is_primary", "sort_order"]

    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

        # 🔥 faqat shu product variantlarini ko‘rsatadi
        if product:
            self.fields["variant"].queryset = product.variants.all()

        # optional qilish
        self.fields["variant"].required = False

        # this is for style(UI)
        widgets = {
            "image": forms.ClearableFileInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
            }),
            "alt_text": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "placeholder": "Image description",
            }),
            "is_primary": forms.CheckboxInput(attrs={
                "class": "h-4 w-4"
            }),
            "sort_order": forms.NumberInput(attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2"
            }),
        }