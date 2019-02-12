import factory
from factory import fuzzy
from wagtailapiimagerendition.models import CustomImage


def create_default_test_image(id=None, title='Test page', file=None):
    image = CustomImage(id=id, title=title, width=120, height=120)
    image.save()

    return image


class CustomImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomImage

    title = fuzzy.FuzzyText()
    file = factory.django.ImageField(color='blue', width = 1200, height = 1200)