from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


def healthcheck_view(request):
    return HttpResponse("OK")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck_view, name="healthcheck"),
    path("users/", include("apps.users.urls", namespace="users")),
    path("shops/", include("apps.shops.urls", namespace="shops")),
    path("", include("apps.catalog.urls", namespace="catalog")),
    path("cart/", include("apps.cart.urls", namespace="cart")),
    path("orders/", include("apps.orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)