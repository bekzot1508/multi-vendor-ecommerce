from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile, SellerProfile, User, UserRole


@receiver(post_save, sender=User)
def create_related_profiles_for_user(sender, instance: User, created: bool, **kwargs):
    """
    User yaratilganda unga mos profilni avtomatik yaratamiz.
    """

    if not created:
        return

    if instance.role == UserRole.CUSTOMER:
        CustomerProfile.objects.create(user=instance)
    elif instance.role == UserRole.SELLER:
        SellerProfile.objects.create(user=instance)