from django.urls import path

from .views import NotificationListView, MarkNotificationReadView

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path(
        "read/<int:notification_id>/",
        MarkNotificationReadView.as_view(),
        name="mark_read",
    ),
]