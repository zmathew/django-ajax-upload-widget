Django Ajax Upload Widget
=========================

Provides AJAX file upload functionality for FileFields and ImageFields with a simple widget replacement in the form.

No change is required your model fields or app logic. This plugin acts transparently so your model forms can treat files as if they were uploaded by "traditional" browser file upload.


Features
--------

* Drop-in replacement for Django's built-in ``ClearableFileInput`` widget (no change required to your model).
* Works in all major browsers including IE 7+.
* Random hash string added to file names to ensure uploaded file paths are not guessable by others.


Usage
-----

Refer to the ``example`` app included in the package for a working example.

Server Side
'''''''''''

In your form, use the ``AjaxClearableFileInput`` on your ``FileField`` or ``ImageField``.
::

    from django import forms
    from ajax_upload.widgets import AjaxClearableFileInput

    class MyForm(forms.Form):
        my_image_field = forms.ImageField(widget=AjaxClearableFileInput())


Or, if using a ``ModelForm`` you can just override the widget.
::

    from django import forms
    from ajax_upload.widgets import AjaxClearableFileInput

    class MyForm(forms.ModelForm):
        class Meta:
            model = MyModel
            widgets = {
                'my_image_field': AjaxClearableFileInput
            }


Client Side
'''''''''''

Just include ``{{ form.media }}`` line in your template for loading all js and css stuff.


JavaScript options
''''''''''''''''''
You can also pass some custom options to JavaScript ``AjaxUploadWidget`` object. For that you may use ``uploader_ops``
optional param:
::

    widgets = {
        'my_image_field': AjaxClearableFileInput(uploader_ops={
            'changeButtonText': "'Click to change'",  # double quotes is required here
            'onError': 'function(data) { alert('Error!'); }'
        })
    }


Using in django admin
'''''''''''''''''''''
An app is completely ready for using in django admin page. It's easy. See an example:
::


    class ProductAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.ImageField: {'widget': AjaxClearableFileInput }
        }


Dependencies
------------
* jQuery 1.7+
* jQuery Iframe Transport plugin (included in this package)


App Installation
----------------

1. Add ``ajax_upload`` to your ``INSTALLED_APPS`` setting.

1. Hook in the urls.
::

    # urls.py
    urlpatterns += patterns('',
        (r'^ajax-upload/', include('ajax_upload.urls')),
    )

1. That's it (don't forget include the jQuery as mentioned above).


Settings
--------

``AJAX_UPLOAD_MAX_FILESIZE`` - Maximum allowed file size in bytes (default: 0).
Setting this greater than 0 will enable validation of uploaded file size.


Running the Tests
-----------------
::

    ./manage.py test ajax_upload


License
-------

This app is licensed under the BSD license. See the LICENSE file for details.
