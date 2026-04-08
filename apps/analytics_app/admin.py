from django.contrib import admin

from .models import DailySalesSnapshot


@admin.register(DailySalesSnapshot)
class DailySalesSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "total_orders",
        "total_revenue",
        "successful_payments",
        "failed_payments",
    )
    ordering = ("-date",)