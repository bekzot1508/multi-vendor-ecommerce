from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from .models import Notification


#***************************
#   Notification list
#***************************
class NotificationListView(LoginRequiredMixin, View):
    template_name = "notifications/notification_list.html"

    def get(self, request):

        notifications = (
            request.user.notifications
            .order_by("-created_at")
        )

        return render(
            request,
            self.template_name,
            {"notifications": notifications},
        )


#***************************
#   Mark as read
#***************************
class MarkNotificationReadView(LoginRequiredMixin, View):

    def post(self, request, notification_id):

        notification = request.user.notifications.get(id=notification_id)

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return redirect("notifications:list")