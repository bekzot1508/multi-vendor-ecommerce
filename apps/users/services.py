from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_with_role(form):
    """
    Registration service.

    View emas, service user yaratadi.
    Keyinchalik DRF qo‘shilganda ham shu service ishlatiladi.
    """

    user = form.save(commit=False)
    user.role = form.cleaned_data["role"]
    user.save()

    return user