from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.orders.models import OrderItem

from .forms import ReviewForm
from .services import create_review_for_order_item


class ReviewCreateView(LoginRequiredMixin, View):
    template_name = "reviews/review_form.html"

    def get(self, request, order_item_id):
        order_item = get_object_or_404(
            OrderItem.objects.select_related("order", "product"),
            id=order_item_id,
            order__user=request.user,
        )

        if hasattr(order_item, "review"):
            messages.info(request, "You already reviewed this item.")
            return redirect("orders:detail", order_id=order_item.order_id)

        form = ReviewForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "order_item": order_item,
            },
        )

    def post(self, request, order_item_id):
        order_item = get_object_or_404(
            OrderItem.objects.select_related("order", "product"),
            id=order_item_id,
            order__user=request.user,
        )

        form = ReviewForm(request.POST)

        if form.is_valid():
            try:
                create_review_for_order_item(
                    user=request.user,
                    order_item=order_item,
                    rating=form.cleaned_data["rating"],
                    comment=form.cleaned_data["comment"],
                )
                messages.success(request, "Review created successfully.")
                return redirect("orders:detail", order_id=order_item.order_id)
            except ValueError as e:
                messages.error(request, str(e))

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "order_item": order_item,
            },
        )