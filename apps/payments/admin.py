from django.contrib import admin

from .models import Payment, PaymentCallbackLog, PaymentTransaction


class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0


class PaymentCallbackLogInline(admin.TabularInline):
    model = PaymentCallbackLog
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "external_reference",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "provider_name")
    search_fields = ("external_reference", "order__order_number")
    inlines = [PaymentTransactionInline, PaymentCallbackLogInline]