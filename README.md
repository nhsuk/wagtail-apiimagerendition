Wagtail - Api image rendition
=============================

Add renditions parameters in cms for images serve through the api.
Provide:
* ImageWithRenditions field that can be use in wagtail model
* ImageWithRenditionsBlock block that can be use in wagtail streamfield

Quick start
-----------

1. Add "wagtailapiimagerendition" to your INSTALLED_APPS setting like this::

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

2. Run `python manage.py migrate` to create the wagtailapiimagerendition models.


How to use ImageWithRenditions field
------------------------------------

In your models.py file (in this example the page models is name CustomPage and the image attribute is header_image)
```python
from wagtailapiimagerendition.fields import ImageWithRenditions
...
class HeaderImageCustomPage(ImageWithRenditions):
    custom_page = ParentalKey('CustomPage', on_delete=models.CASCADE, related_name='header_image')
...
```



How to use ImageWithRenditionsBlock block
-----------------------------------------

In your models.py file (in this example the page models is name CustomPage and the image attribute is header_image)
```python
from wagtailapiimagerendition.blocks import ImageWithRenditionsBlock
...
class CustomPage(Page):
    body = StreamField([
        ('image', ImageWithRenditionsBlock()),
    ], null=True, blank=True)
...
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