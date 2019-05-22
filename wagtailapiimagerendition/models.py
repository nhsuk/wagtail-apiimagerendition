"""
.. module:: wagtailapiimagerendition.models
"""

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    """ CustomImage """
    admin_form_fields = Image.admin_form_fields + ()

    @property
    def link(self):
        """ link """
        if self.file:
            return self.file.url
        else:
            return ''

    def generate_and_get_rendition(self, rendition_size):
        """ generate_and_get_rendition """
        if not self.file or rendition_size == 'none':
            return self.file.url
        else:
            return self.get_rendition('fill-{}'.format(rendition_size)).url

    def save(self, *args, **kwargs):
        """ save """
        super(CustomImage, self).save(*args, **kwargs)


class ImageRendition(AbstractRendition):
    """ ImageRendition """
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
@receiver(post_delete, sender=ImageRendition)
def image_delete(sender, instance, **kwargs):
    """ image_delete """
    instance.file.delete(False)
