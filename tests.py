import json
from PIL import Image

from django.test import Client

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

from dummy_page.models import CustomPage, HeaderImageCustomPage
from wagtailapiimagerendition.factories import CustomImageFactory


class ImageRenditionClassTests(WagtailPageTests):

    def test_rendition_image_field_original(self):
        image = CustomImageFactory()

        custom_page = CustomPage(title='test', slug='test')
        parent_page = Page.objects.get(id=2)
        parent_page.add_child(instance=custom_page)
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

        desktop_header_image = Image.open('./{}'.format(content['header_image'][0]['desktop_image']))
        width, height = desktop_header_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)

        mobile_header_image = Image.open('./{}'.format(content['header_image'][0]['mobile_image']))
        width, height = mobile_header_image.size
        self.assertEqual(width, 1200)
        self.assertEqual(height, 1200)


    def test_rendition_image_field_custom(self):
        image = CustomImageFactory()

        custom_page = CustomPage(title='test', slug='test')
        parent_page = Page.objects.get(id=2)
        parent_page.add_child(instance=custom_page)
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

        desktop_header_image = Image.open('./{}'.format(content['header_image'][0]['desktop_image']))
        width, height = desktop_header_image.size
        self.assertEqual(width, 400)
        self.assertEqual(height, 800)

        mobile_header_image = Image.open('./{}'.format(content['header_image'][0]['mobile_image']))
        width, height = mobile_header_image.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 200)
