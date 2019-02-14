import json
from PIL import Image

from django.test import Client

from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.blocks.struct_block import StructValue
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from dummy_page.models import CustomPage, HeaderImageCustomPage
from wagtailapiimagerendition.factories import CustomImageFactory
from wagtailapiimagerendition.blocks import ImageWithRenditionsBlock

class ImageRenditionClassTests(WagtailPageTests):

    def test_rendition_image_field_original(self):
        image = CustomImageFactory()

        custom_page = CustomPage(title='test', slug='test')
        parent_page = Page.objects.get(id=2)
        parent_page.add_child(instance=custom_page)
        field = CustomPage._meta.get_field('body')
        custom_page.body = StreamValue(field.stream_block, [
            ('image', StructValue(ImageWithRenditionsBlock, [
                ('image', image),
                ('meta_mobile_rendition', 'none'),
                ('meta_desktop_rendition', 'none'),
            ]))
        ])
        custom_page.save()

        image_with_renditions = HeaderImageCustomPage(
            image=image,
            image_mobile_rendition='none',
            image_desktop_rendition='none',
            custom_page=custom_page,
        )
        image_with_renditions.save()

        c = Client()
        response = c.get('/api/v2/pages/{}/'.format(custom_page.id))

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertEqual(len(content['header_image']), 1)

        mobile_header_image = Image.open('./{}'.format(content['header_image'][0]['mobile_image']))
        width, height = mobile_header_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        desktop_header_image = Image.open('./{}'.format(content['header_image'][0]['desktop_image']))
        width, height = desktop_header_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        mobile_body_image = Image.open('./{}'.format(content['body'][0]['value']['renditions']['mobile']))
        width, height = mobile_body_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        desktop_body_image = Image.open('./{}'.format(content['body'][0]['value']['renditions']['desktop']))
        width, height = desktop_body_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)


    def test_rendition_image_field_custom(self):
        image = CustomImageFactory()

        custom_page = CustomPage(title='test', slug='test')
        parent_page = Page.objects.get(id=2)
        parent_page.add_child(instance=custom_page)
        field = CustomPage._meta.get_field('body')
        custom_page.body = StreamValue(field.stream_block, [
            ('image', StructValue(ImageWithRenditionsBlock, [
                ('image', image),
                ('meta_mobile_rendition', '100x50'),
                ('meta_desktop_rendition', '400x200'),
            ]))
        ])
        custom_page.save()

        image_with_renditions = HeaderImageCustomPage(
            image=image,
            image_mobile_rendition='100x200',
            image_desktop_rendition='400x800',
            custom_page=custom_page,
        )
        image_with_renditions.save()

        c = Client()
        response = c.get('/api/v2/pages/{}/'.format(custom_page.id))

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertEqual(len(content['header_image']), 1)

        mobile_header_image = Image.open('./{}'.format(content['header_image'][0]['mobile_image']))
        width, height = mobile_header_image.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 200)

        desktop_header_image = Image.open('./{}'.format(content['header_image'][0]['desktop_image']))
        width, height = desktop_header_image.size
        self.assertEqual(width, 400)
        self.assertEqual(height, 800)

        mobile_body_image = Image.open('./{}'.format(content['body'][0]['value']['renditions']['mobile']))
        width, height = mobile_body_image.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 50)

        desktop_body_image = Image.open('./{}'.format(content['body'][0]['value']['renditions']['desktop']))
        width, height = desktop_body_image.size
        self.assertEqual(width, 400)
        self.assertEqual(height, 200)