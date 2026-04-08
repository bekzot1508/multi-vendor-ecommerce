from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Address, User, UserRole


class RegisterForm(UserCreationForm):
    """
    User registration form.

    Role tanlash imkoniyati bor:
    - customer
    - seller
    """

    role = forms.ChoiceField(
        choices=[
            (UserRole.CUSTOMER, "Customer"),
            (UserRole.SELLER, "Seller"),
        ],
        initial=UserRole.CUSTOMER,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "full_name",
            "role",
            "password1",
            "password2",
        )

    # this is for style(UI)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full rounded-lg border border-gray-300 px-3 py-2 "
                "focus:outline-none focus:ring-2 focus:ring-blue-500"
            )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 text-gray-800 placeholder-gray-400 outline-none focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-100",
            "placeholder": "Enter your username",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 text-gray-800 placeholder-gray-400 outline-none focus:border-indigo-500 focus:bg-white focus:ring-4 focus:ring-indigo-100",
            "placeholder": "Enter your password",
        })
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("user",)