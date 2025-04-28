from django.db import models
from django.utils.text import slugify

from apps.accounts.models import Contact
from apps.core.models.ownership import City
from apps.product.models import ProductCategory


# Create your models here.
class Driver(models.Model):

    contact = models.ManyToManyField(Contact, default=[], blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.contact.name

    def save(
        self,
        *args,
        **kwargs,
    ):

        if not self.slug:
            self.slug = slugify(self.contact.name)

        super().save(*args, **kwargs)


class Car(models.Model):

    prefix_number = models.IntegerField(default=11)
    alphabet = models.CharField(max_length=2, default='ط')
    postfix_number = models.IntegerField(default=111)
    city_code = models.ForeignKey(City, on_delete=models.PROTECT)

    has_refrigerator = models.BooleanField(default=False)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)

    slug = models.SlugField(unique=True)
    repetitive = models.BooleanField(default=False)

    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.prefix_number}{self.alphabet}{self.postfix_number}/{self.city_code.car_code}'

    def save(
            self,
            *args,
            **kwargs,
    ):
        if not self.slug:
            self.slug = slugify(f'{self.prefix_number}{self.alphabet}{self.postfix_number}{self.city_code.car_code}')

        super().save(*args, **kwargs)
