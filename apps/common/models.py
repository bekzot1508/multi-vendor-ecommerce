from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    """
    Abstract base model.

    created_at va updated_at fieldlarni har safar qayta yozmaslik uchun ishlatiladi.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True