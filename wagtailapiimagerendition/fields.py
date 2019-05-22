"""
.. module:: wagtailapiimagerendition.fields
"""

from django.db import models
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.images.edit_handlers import ImageChooserPanel


MOBILE_RENDITION_CHOICES = (
    ('none', 'Use Original'),
)

DESKTOP_RENDITION_CHOICES = (
    ('none', 'Use Original'),
)

if hasattr(settings, 'MOBILE_RENDITION_CHOICES'):
    MOBILE_RENDITION_CHOICES = settings.MOBILE_RENDITION_CHOICES

if hasattr(settings, 'DESKTOP_RENDITION_CHOICES'):
    DESKTOP_RENDITION_CHOICES = settings.DESKTOP_RENDITION_CHOICES


class ImageWithRenditions(models.Model):
    """ ImageWithRenditions """
    image = models.ForeignKey(
        'wagtailapiimagerendition.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_mobile_rendition = models.CharField(
        choices=MOBILE_RENDITION_CHOICES,
        verbose_name='Mobile Rendition',
        default='none',
        max_length=10,
    )
    image_desktop_rendition = models.CharField(
        choices=DESKTOP_RENDITION_CHOICES,
        verbose_name='Desktop Rendition',
        default='none',
        max_length=10,
    )

    @property
    def mobile_image(self):
        """ mobile_image """
        return self.image.generate_and_get_rendition(self.image_mobile_rendition)

    @property
    def desktop_image(self):
        """ desktop_image """
        return self.image.generate_and_get_rendition(self.image_desktop_rendition)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('image_mobile_rendition'),
        FieldPanel('image_desktop_rendition'),
    ]

    api_fields = [
        APIField('mobile_image'),
        APIField('desktop_image'),
    ]

    class Meta:
        """ Meta """
        abstract = True
