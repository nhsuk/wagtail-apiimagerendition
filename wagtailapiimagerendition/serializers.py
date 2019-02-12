from rest_framework import serializers

from .models import CustomImage


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomImage
        fields = ()