from distutils.core import setup

import ajax_upload


setup(
    name='django-ajax-upload-widget',
    packages=['ajax_upload', 'ajax_upload.tests'],
    version=ajax_upload.__version__,
    description=ajax_upload.__doc__,
    long_description=open('README.rst').read(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    author='Zach Mathew',
    url='http://github.com/zmathew/django-ajax-upload-widget',
    license='BSD',
)
