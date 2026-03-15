import factory
from django.contrib.auth import get_user_model

from apps.users.models import UserRole

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker("name")
    role = UserRole.CUSTOMER