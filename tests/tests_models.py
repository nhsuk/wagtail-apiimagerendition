"""
.. module:: tests
"""

from PIL import Image
import json
import os
import re

from django.test import Client

from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.blocks.struct_block import StructValue
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from test_page.factories import CustomImageFactory
from test_page.models import CustomImageRendition, TestPage, HeaderImageTestPage
from wagtailapiimagerendition.blocks import ImageWithRenditionsBlock


class CustomImageRenditionClassTests(WagtailPageTests):
    """ CustomImageRenditionClassTests """

    def test_custom_image_link(self):
        """ test_custom_image_link """
        image = CustomImageFactory()
        self.assertRegex(image.link, r'^/media/original_images/example.jpg$')

        image.file.delete(False)
        self.assertEqual(image.link, '')
        image.delete()

    def test_image_delete_file(self):
        """ test_image_delete_file """
        image = CustomImageFactory()
        file = image.file.path
        image.generate_and_get_rendition('100x50')
        image_rendition = CustomImageRendition.objects.get(image=image)
        file_rendition = image_rendition.file.path
        self.assertTrue(os.path.exists(file))
        self.assertTrue(os.path.exists(file_rendition))

        image.delete()
        self.assertFalse(os.path.exists(file))
        self.assertFalse(os.path.exists(file_rendition))

    def test_rendition_image_field_original(self):
        """ test_rendition_image_field_original """
        image = CustomImageFactory()

        test_page = TestPage(title='test', slug='test')
        parent_page = Page.objects.get(id=2)
        parent_page.add_child(instance=test_page)
        field = TestPage._meta.get_field('body')
        test_page.body = StreamValue(field.stream_block, [
            ('image', StructValue(ImageWithRenditionsBlock, [
                ('image', image),
                ('meta_mobile_rendition', 'none'),
                ('meta_desktop_rendition', 'none'),
            ]))
        ])
        test_page.save()

        image_with_renditions = HeaderImageTestPage(
            image=image,
            image_mobile_rendition='none',
            image_desktop_rendition='none',
            test_page=test_page,
        )
        image_with_renditions.save()

        c = Client()
        response = c.get('/api/v2/pages/{}/'.format(test_page.id))

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertEqual(len(content['header_image']), 1)

        mobile_header_image = Image.open('./{}'.format(content['header_image'][0]['mobile_image']))
        width, height = mobile_header_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        desktop_header_image = Image.open('./{}'.format(
            content['header_image'][0]['desktop_image']))
        width, height = desktop_header_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        mobile_body_image = Image.open('./{}'.format(
            content['body'][0]['value']['renditions']['mobile']))
        width, height = mobile_body_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        desktop_body_image = Image.open('./{}'.format(
            content['body'][0]['value']['renditions']['desktop']))
        width, height = desktop_body_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        with self.settings(LOCAL_ASSET_FULL_PATH=True):
            self.assertEqual(
                image_with_renditions.mobile_image,
                'http://localhost:8000/media/original_images/example.jpg',
            )
            self.assertEqual(
                image_with_renditions.desktop_image,
                'http://localhost:8000/media/original_images/example.jpg',
            )
            c = Client()
            response = c.get('/api/v2/pages/{}/'.format(test_page.id))
            self.assertEqual(response.status_code, 200)
            content = json.loads(response.content)
            self.assertEqual(
                content['body'][0]['value']['renditions']['mobile'],
                'http://localhost:8000/media/original_images/example.jpg',
            )
            self.assertEqual(
                content['body'][0]['value']['renditions']['desktop'],
                'http://localhost:8000/media/original_images/example.jpg',
            )

        image.delete()

    def test_rendition_image_field_custom(self):
        """ test_rendition_image_field_custom """
        image = CustomImageFactory()

        test_page = TestPage(title='test', slug='test')
        parent_page = Page.objects.get(id=2)
        parent_page.add_child(instance=test_page)
        field = TestPage._meta.get_field('body')
        test_page.body = StreamValue(field.stream_block, [
            ('image', StructValue(ImageWithRenditionsBlock, [
                ('image', image),
                ('meta_mobile_rendition', '100x50'),
                ('meta_desktop_rendition', '400x200'),
            ]))
        ])
        test_page.save()

        image_with_renditions = HeaderImageTestPage(
            image=image,
            image_mobile_rendition='100x200',
            image_desktop_rendition='400x800',
            test_page=test_page,
        )
        image_with_renditions.save()

        c = Client()
        response = c.get('/api/v2/pages/{}/'.format(test_page.id))

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertEqual(len(content['header_image']), 1)

        mobile_header_image = Image.open('./{}'.format(content['header_image'][0]['mobile_image']))
        width, height = mobile_header_image.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 200)

        desktop_header_image = Image.open('./{}'.format(
            content['header_image'][0]['desktop_image']))
        width, height = desktop_header_image.size
        self.assertEqual(width, 400)
        self.assertEqual(height, 800)

        mobile_body_image = Image.open('./{}'.format(
            content['body'][0]['value']['renditions']['mobile']))
        width, height = mobile_body_image.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 50)

        desktop_body_image = Image.open('./{}'.format(
            content['body'][0]['value']['renditions']['desktop']))
        width, height = desktop_body_image.size
        self.assertEqual(width, 400)
        self.assertEqual(height, 200)


        with self.settings(LOCAL_ASSET_FULL_PATH=True):
            regexp = re.compile('^http\:\/\/localhost\:8000\/media\/images\/example\.[A-z0-9]+\.fill-[0-9]+x[0-9]+\.jpg$')
            self.assertIsNotNone(
                regexp.match(image_with_renditions.mobile_image)
            )
            self.assertIsNotNone(
                regexp.match(image_with_renditions.desktop_image)
            )

            c = Client()
            response = c.get('/api/v2/pages/{}/'.format(test_page.id))
            self.assertEqual(response.status_code, 200)
            content = json.loads(response.content)
            self.assertIsNotNone(
                regexp.match(content['body'][0]['value']['renditions']['mobile'])
            )
            self.assertIsNotNone(
                regexp.match(content['body'][0]['value']['renditions']['desktop'])
            )

        image.delete()

    def test_rendition_image_block_definition(self):
        """ test_rendition_image_field_original """
        image_block = ImageWithRenditionsBlock()
        definition = image_block.get_definition()

        self.assertTrue(definition['collapsible'])
        self.assertFalse(definition['closed'])
        self.assertEqual(definition['tabs'], [{
            'key': 'content',
            'label': 'Content',
            'fields': ['image'],
        }, {
            'key': 'settings',
            'label': 'Settings',
            'fields': ['meta_mobile_rendition', 'meta_desktop_rendition'],
        }])
