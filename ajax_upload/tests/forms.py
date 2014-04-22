from django import forms

from ajax_upload.widgets import AjaxClearableFileInput


class TestForm(forms.Form):
    my_file = forms.FileField(required=False, widget=AjaxClearableFileInput)
    my_image = forms.ImageField(required=False, widget=AjaxClearableFileInput)
