from django import forms

from .models import Shop


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ("name", "description", "logo")