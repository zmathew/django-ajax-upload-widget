

from django.contrib import admin
from django.db import models
from ajax_upload.widgets import AjaxClearableFileInput

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AjaxClearableFileInput }
    }

admin.site.register(Product, ProductAdmin)