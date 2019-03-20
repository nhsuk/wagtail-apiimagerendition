Wagtail - Api image rendition
=============================

Add renditions parameters in cms for images serve through the api.
Provide:
* ImageWithRenditions field that can be use in wagtail model
* ImageWithRenditionsBlock block that can be use in wagtail streamfield

Quick start
-----------

1. Add "wagtailapiimagerendition" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
    'wagtailapiimagerendition',
    ...
]
```

2. Add MOBILE_RENDITION_CHOICES and DESKTOP_RENDITION_CHOICES settings (example)
```python
MOBILE_RENDITION_CHOICES = (
    ('none', 'Use Original'),
    ('100x50', '100 x 50'),
    ('100x200', '100 x 200'),
    ('150x150', '150 x 150'),
)

DESKTOP_RENDITION_CHOICES = (
    ('none', 'Use Original'),
    ('400x200', '400 x 200'),
    ('400x800', '400 x 800'),
    ('600x600', '600 x 600'),
)
```

3. Run `python manage.py migrate` to create the wagtailapiimagerendition models.


How to use ImageWithRenditions field
------------------------------------

In your models.py file (in this example the page models is name TestPage and the image attribute is header_image)
```python
from wagtailapiimagerendition.fields import ImageWithRenditions
...
class HeaderImageTestPage(ImageWithRenditions):
    test_page = ParentalKey('TestPage', on_delete=models.CASCADE, related_name='header_image')
...
```

API output exmaple:
```json
{
    ...
    "header_image": [{
        "id": 1,
        "meta": {
            "type": "test_page.HeaderImageTestPage"
        },
        "mobile_image": "/media/images/example_X257M1O.2e16d0ba.fill-100x200.jpg",
        "desktop_image": "/media/images/example_X257M1O.2e16d0ba.fill-400x800.jpg"
    }],
    ...
}
```


How to use ImageWithRenditionsBlock block
-----------------------------------------

In your models.py file (in this example the page models is name TestPage and the image attribute is header_image)
```python
from wagtailapiimagerendition.blocks import ImageWithRenditionsBlock
...
class TestPage(Page):
    body = StreamField([
        ('image', ImageWithRenditionsBlock()),
    ], null=True, blank=True)
...
```

API output exmaple:
```json
{
    ...
    "body": [{
        "type": "image",
        "value": {
            "renditions": {
                "mobile": "/media/images/example_X257M1O.2e16d0ba.fill-100x50.jpg",
                "desktop": "/media/images/example_X257M1O.2e16d0ba.fill-400_x_200.jpg"
            }
        },
        "id": "3edd3c13-d211-41ef-acf0-2a30bd57042c"
    }]
    ...
}
```

How to contribute
-----------------

### Requirements
* Docker
* docker-compose
You'll get all this lot installed nicely with (https://docs.docker.com/docker-for-mac/install).


### Setup locally
Build the image
```
docker-compose build
```
Run the containers
```
docker-compose up
```
Create super user:
```
docker-compose run --rm web python manage.py createsuperuser
```