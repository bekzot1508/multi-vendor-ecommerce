from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from apps.catalog.views import HomeView


def healthcheck_view(request):
    return HttpResponse("OK")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck_view, name="healthcheck"),

    path("", HomeView.as_view(), name="home"),
    path("users/", include("apps.users.urls", namespace="users")),
    path("shops/", include("apps.shops.urls", namespace="shops")),
    path("", include("apps.catalog.urls", namespace="catalog")),
    path("cart/", include("apps.cart.urls", namespace="cart")),
    path("orders/", include("apps.orders.urls", namespace="orders")),
    path("payments/", include("apps.payments.urls", namespace="payments")),
    path("notifications/", include("apps.notifications.urls", namespace="notifications")),
    path("shipping/", include("apps.shipping.urls", namespace="shipping")),
    path("reviews/", include("apps.reviews.urls", namespace="reviews")),
    path("analytics/", include("apps.analytics_app.urls", namespace="analytics")),
    path("inventory/", include("apps.inventory.urls", namespace="inventory")),
    path("payouts/", include("apps.payouts.urls", namespace="payouts")),
    path("backoffice/", include("apps.backoffice.urls", namespace="backoffice")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)