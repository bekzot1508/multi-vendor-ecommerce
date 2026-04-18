from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.users.models import UserRole

from .forms import ShopCreateForm
from .models import Shop, ShopStatus


#********************
#   shop create views
#********************
class ShopCreateView(LoginRequiredMixin, View):
    template_name = "shops/shop_create.html"

    def dispatch(self, request, *args, **kwargs):
        # Faqat sellerlar shop yaratishi mumkin
        if request.user.role != UserRole.SELLER:
            messages.error(request, "Only sellers can create shops.")
            return redirect("users:profile")
        elif request.user.seller_profile.is_approved == False:
            messages.error(request, "You are not approved to create Shop.")
            return redirect("users:profile")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = ShopCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ShopCreateForm(request.POST, request.FILES)

        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.status = ShopStatus.PENDING
            shop.save()

            messages.success(
                request,
                "Shop created. Waiting for admin approval.",
            )

            return redirect("users:profile")

        return render(request, self.template_name, {"form": form})