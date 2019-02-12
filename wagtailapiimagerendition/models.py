import operator
from functools import reduce

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver

from wagtail.core.models import PageRevision
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    admin_form_fields = Image.admin_form_fields + ()
    
    @property
    def link(self):
        if self.file:
            return self.file.url
        else:
            return ''

    def generate_and_get_rendition(self, rendition_size):
        if not self.file or rendition_size == 'none':
            return self.file.url
        else:
            return self.get_rendition('fill-{}'.format(rendition_size)).url

    def save(self, *args, **kwargs):
        super(CustomImage, self).save(*args, **kwargs)


class ImageRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        related_name='renditions',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(post_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(post_delete, sender=ImageRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
