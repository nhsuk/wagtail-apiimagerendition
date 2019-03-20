from modelcluster.fields import ParentalKey

from django.db import models

from wagtail.admin.edit_handlers import StreamFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailapiimagerendition.blocks import ImageWithRenditionsBlock
from wagtailapiimagerendition.fields import ImageWithRenditions


class HeaderImageTestPage(ImageWithRenditions):
    test_page = ParentalKey('TestPage', on_delete=models.CASCADE, related_name='header_image')


class TestPage(Page):
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
