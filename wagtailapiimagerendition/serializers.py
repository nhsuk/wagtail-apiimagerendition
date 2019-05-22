"""
.. module:: wagtailapiimagerendition.serializers
"""
from rest_framework import serializers

from .models import CustomImage


class ImageSerializer(serializers.ModelSerializer):
    """ ImageSerializer """

    class Meta:
        """ Meta """
        model = CustomImage
        fields = ()
