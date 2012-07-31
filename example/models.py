from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='examples/', blank=True)
