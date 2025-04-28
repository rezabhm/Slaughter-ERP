from django.db import models
from django.utils.text import slugify


# Create your models here.
class Unit(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class ProductCategory(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(
        self,
        *args,
        **kwargs
    ):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=120)

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    unit = models.ManyToManyField(Unit, default=[])

    slug = models.SlugField(unique=True)

    def save(
        self,
        *args,
        **kwargs,
    ):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
