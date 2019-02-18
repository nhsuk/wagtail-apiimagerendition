from os import path
from setuptools import find_packages, setup
from wagtailapiimagerendition import __VERSION__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wagtail-apiimagerendition',
    version=__VERSION__,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/yohanlebret/wagtail-apiimagerendition',
    license='MIT',
    description='Add renditions parameters in cms for images serve through the api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yohan Lebret',
    author_email='yohan.lebret@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)