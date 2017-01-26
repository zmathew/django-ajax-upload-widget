

from django.contrib import admin
from django.db import models
from ajax_upload.widgets import AjaxClearableFileInput

from .models import Product, SubProduct


class SubProductInLine(admin.StackedInline):
    model = SubProduct
    formfield_overrides = {
        models.ImageField: {'widget': AjaxClearableFileInput }
    }
    extra = 0

    class Media:
        js = ['ajax_upload/js/ajax-upload-admin-inline-hook.js']


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AjaxClearableFileInput }
    }
    inlines = [SubProductInLine, ]

admin.site.register(Product, ProductAdmin)