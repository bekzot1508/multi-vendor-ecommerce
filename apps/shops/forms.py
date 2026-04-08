from django import forms

from .models import Shop


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["name", "description", "logo"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 outline-none",
                "placeholder": "Enter shop name"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 outline-none",
                "rows": 4,
                "placeholder": "Describe your shop..."
            }),
            "logo": forms.FileInput(attrs={
                "class": "w-full border border-gray-300 rounded-xl px-3 py-2 bg-gray-50"
            })
        }