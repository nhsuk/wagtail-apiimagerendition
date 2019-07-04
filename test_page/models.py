"""
.. module:: test_page.models
"""

from modelcluster.fields import ParentalKey

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from wagtailapiimagerendition.blocks import ImageWithRenditionsBlock
from wagtailapiimagerendition.fields import ImageWithRenditions
from wagtailapiimagerendition.models import WithApiRenditionMixin


class CustomImage(AbstractImage, WithApiRenditionMixin):
    admin_form_fields = Image.admin_form_fields + ()


class CustomImageRendition(AbstractRendition):
    """ CustomImageRendition """
    image = models.ForeignKey(
        CustomImage,
        related_name='renditions',
        on_delete=models.CASCADE,
    )

    class Meta:
        """ Meta """
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(post_delete, sender=CustomImage)
@receiver(post_delete, sender=CustomImageRendition)
def image_delete(sender, instance, **kwargs):
    """ image_delete """
    instance.file.delete(False)


class HeaderImageTestPage(ImageWithRenditions):
    """ HeaderImageTestPage """
    test_page = ParentalKey('TestPage', on_delete=models.CASCADE, related_name='header_image')


class TestPage(Page):
    """ TestPage """
    body = StreamField([
        ('image', ImageWithRenditionsBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('header_image', label='Header Image', min_num=0, max_num=1),
        StreamFieldPanel('body'),
    ]

    api_fields = [
        APIField('header_image'),
        APIField('body'),
    ]
