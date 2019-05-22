"""
.. module:: wagtailapiimagerendition.factories
"""

import factory
from factory import fuzzy
from wagtailapiimagerendition.models import CustomImage


class CustomImageFactory(factory.django.DjangoModelFactory):
    """ CustomImageFactory """
    class Meta:
        """ Meta """
        model = CustomImage

    title = fuzzy.FuzzyText()
    file = factory.django.ImageField(color='blue', width=1200, height=1200)
