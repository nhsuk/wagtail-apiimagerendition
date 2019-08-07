"""
.. module:: wagtailapiimagerendition.block
"""

from django.conf import settings

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageWithRenditionsBlock(blocks.StructBlock):
    """ImageWithRenditionsBlock """
    _content_fields = ['image']
    _settings_fields = ['meta_mobile_rendition', 'meta_desktop_rendition']

    image = ImageChooserBlock(required=False)
    meta_mobile_rendition = blocks.ChoiceBlock(
        settings.MOBILE_RENDITION_CHOICES,
        label='Mobile Rendition',
        default='none',
    )
    meta_desktop_rendition = blocks.ChoiceBlock(
        settings.DESKTOP_RENDITION_CHOICES,
        label='Desktop Rendition',
        default='none',
    )

    class Meta:
        icon = 'image'

    def get_api_representation(self, value, context=None):
        """ get_api_representation """
        result = blocks.StructBlock.get_api_representation(self, value, context)

        if 'image' in result:
            image = {}
            meta_mobile_rendition = result['meta_mobile_rendition']
            meta_desktop_rendition = result['meta_desktop_rendition']

            mobile_image = value['image'].generate_and_get_rendition(meta_mobile_rendition) \
                if value['image'] else None
            desktop_image = value['image'].generate_and_get_rendition(meta_desktop_rendition) \
                if value['image'] else None

            if hasattr(settings, 'LOCAL_ASSET_FULL_PATH') and settings.LOCAL_ASSET_FULL_PATH:
                if mobile_image:
                    mobile_image = 'http://localhost:8000{0}'.format(mobile_image)
                if desktop_image:
                    desktop_image = 'http://localhost:8000{0}'.format(desktop_image)

            image['renditions'] = {
                'mobile': mobile_image,
                'desktop': desktop_image,
            }
        return image

    def get_tabs_definition(self):
        return {
            'content': {
                'key': 'content',
                'label': 'Content',
                'fields': self.__class__._content_fields,
            },
            'settings': {
                'key': 'settings',
                'label': 'Settings',
                'fields': self.__class__._settings_fields,
            },
        }

    def get_definition(self):
        definition = super().get_definition()
        definition['collapsible'] = True
        definition['closed'] = False

        # Add tabs
        definition['tabs'] = []
        tabs = self.get_tabs_definition()
        for tab_name in ['content', 'settings']:
            definition['tabs'].append(tabs[tab_name])

        return definition
