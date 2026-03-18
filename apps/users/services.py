from django.contrib.auth import get_user_model

from .models import UserRole

User = get_user_model()


def create_user_with_role(form):
    """
    Public registration service.

    Double security:
    - form faqat customer/seller ko‘rsatadi
    - service esa admin rolni qat'iyan bloklaydi
    """

    selected_role = form.cleaned_data["role"]

    if selected_role not in [UserRole.CUSTOMER, UserRole.SELLER]:
        selected_role = UserRole.CUSTOMER

    user = form.save(commit=False)
    user.role = selected_role

    # Public registration orqali hech qachon staff/superuser bo‘lmasin
    user.is_staff = False
    user.is_superuser = False

    user.save()
    return user