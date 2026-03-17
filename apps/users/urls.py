from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("profile/", views.ProfileView.as_view(), name="profile"),

    # Address CRUD
    path("addresses/", views.AddressListView.as_view(), name="address_list"),
    path("addresses/create/", views.AddressCreateView.as_view(), name="address_create"),
    path("addresses/<int:pk>/edit/", views.AddressUpdateView.as_view(), name="address_edit"),
    path("addresses/<int:pk>/delete/", views.AddressDeleteView.as_view(), name="address_delete"),
]