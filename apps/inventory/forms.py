from django import forms


class InventoryUpdateForm(forms.Form):
    total_stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }
        ),
    )
    low_stock_threshold = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
            }
        ),
    )
    note = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2",
                "placeholder": "Reason for stock update",
            }
        ),
    )