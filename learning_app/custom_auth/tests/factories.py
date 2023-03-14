import factory
from custom_auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    document_number = factory.Faker("ean")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
