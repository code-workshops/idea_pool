import factory.fuzzy

from accounts.factories import UserFactory
from .models import Idea


# pylint: disable=missing-docstring
class IdeaFactory(factory.DjangoModelFactory):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = Idea

    content = factory.fuzzy.FuzzyText(prefix='Idea | ')
    impact = factory.fuzzy.FuzzyInteger(1,10)
    ease = factory.fuzzy.FuzzyInteger(1,10)
    confidence = factory.fuzzy.FuzzyInteger(1,10)
    user = factory.SubFactory(UserFactory)
