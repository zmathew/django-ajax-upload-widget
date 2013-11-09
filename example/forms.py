from django import forms

from ajax_upload.widgets import AjaxClearableFileInput

from example.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
            'image': AjaxClearableFileInput
        }
