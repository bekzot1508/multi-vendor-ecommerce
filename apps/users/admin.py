from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Address, CustomerProfile, SellerProfile, User

# Register your models here.



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    )
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "full_name")
    ordering = ("-created_at",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Business fields",
            {
                "fields": (
                    "full_name",
                    "role",
                )
            },
        ),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "created_at")
    search_fields = ("user__username", "user__email", "phone")


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "is_approved", "approved_at", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("user__username", "user__email", "phone")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        "country",
        "city",
        "is_default_shipping",
        "is_default_billing",
    )
    list_filter = ("country", "city", "is_default_shipping", "is_default_billing")
    search_fields = ("user__username", "user__email", "full_name", "phone", "city")