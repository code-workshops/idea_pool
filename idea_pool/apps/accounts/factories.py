import factory

from .models import User


# pylint: disable=missing-docstring
class UserFactory(factory.DjangoModelFactory):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = User

    username = factory.Faker('name')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    password = 'password'
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)
