from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import AddressForm, LoginForm, RegisterForm
from .models import Address
from .services import create_user_with_role


#*************************
#   redirect helper
#*************************
def redirect_after_login(user):
    if user.role == "seller":
        return "users:profile"
    return "home"


#*************************
#   register views
#*************************
class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = create_user_with_role(form)

            login(request, user)
            messages.success(request, "Registration successful.")
            login(request, user)
            return redirect(redirect_after_login(user))

        return render(request, self.template_name, {"form": form})


#*************************
#   login views
#*************************
class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Logged in successfully.")
            login(request, user)
            return redirect(redirect_after_login(user))

        return render(request, self.template_name, {"form": form})


#*************************
#   logout views
#*************************
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("users:login")


#*************************
#   profile views
#*************************
class ProfileView(LoginRequiredMixin, View):
    template_name = "users/profile.html"

    def get(self, request):
        return render(request, self.template_name)


#**********************************************
#   ADDRESS CRUD
#   address list views
#**********************************************
class AddressListView(LoginRequiredMixin, View):
    template_name = "users/address_list.html"

    def get(self, request):
        addresses = request.user.addresses.all()
        return render(request, self.template_name, {"addresses": addresses})


#*************************
#   address create views
#*************************
class AddressCreateView(LoginRequiredMixin, View):
    template_name = "users/address_form.html"

    def get(self, request):
        form = AddressForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            messages.success(request, "Address added.")
            return redirect("users:address_list")

        return render(request, self.template_name, {"form": form})

#*************************
#   address update views
#*************************
class AddressUpdateView(LoginRequiredMixin, View):
    template_name = "users/address_form.html"

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        form = AddressForm(instance=address)

        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            messages.success(request, "Address updated.")
            return redirect("users:address_list")

        return render(request, self.template_name, {"form": form})


#*************************
#   address delete views
#*************************
class AddressDeleteView(LoginRequiredMixin, View):
    template_name = "users/address_confirm_delete.html"

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        return render(request, self.template_name, {"address": address})

    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.delete()

        messages.success(request, "Address deleted.")
        return redirect("users:address_list")