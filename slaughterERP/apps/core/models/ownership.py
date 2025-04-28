from django.db import models
from django.utils.text import slugify

from apps.accounts.models import Contact


# models
class City(models.Model):

    name = models.CharField(max_length=50)
    car_code = models.IntegerField(default=11)
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


class Agriculture(models.Model):

    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
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


class ProductOwner(models.Model):

    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.contact.name

    def save(
            self,
            *args,
            **kwargs
    ):
        if not self.slug:
            self.slug = slugify(self.contact.name)

        super().save(*args, **kwargs)
