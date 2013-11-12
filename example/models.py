from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='examples/', blank=True)


class SubProduct(models.Model):
    """
    Useless model just for inlines testing
    """
    parent = models.ForeignKey(Product)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='examples/', blank=True)
