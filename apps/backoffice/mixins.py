from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class BackofficeAccessMixin(LoginRequiredMixin):
    """
    Custom admin/backoffice panel faqat admin/staff userlar uchun.

    Security rule:
    - oddiy customer kira olmaydi
    - seller kira olmaydi
    - role=admin bo‘lishi va is_staff=True bo‘lishi kerak
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return self.handle_no_permission()

        if user.role != "admin" or not user.is_staff:
            messages.error(request, "You do not have access to the backoffice panel.")
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)