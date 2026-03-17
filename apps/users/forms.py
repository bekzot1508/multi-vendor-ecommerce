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
        choices=UserRole.choices,
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


class LoginForm(AuthenticationForm):
    """
    Default Django login formni ishlatamiz,
    lekin keyin custom UI uchun override qilish oson.
    """

    username = forms.CharField(max_length=150)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("user",)