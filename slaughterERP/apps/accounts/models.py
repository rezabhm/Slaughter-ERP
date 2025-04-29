from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from apps.product.models import Unit


# Create your models here.
class Role(models.Model):

    role_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    unit = models.ManyToManyField(Unit, default=[])

    def __str__(self):
        return self.role_name


class CustomUser(AbstractUser):

    role = models.ManyToManyField(Role, default=[])

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):

        if not self.password:

            self.set_password('1234')

        super().save(*args, **kwargs)


class Contact(models.Model):

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    unit = models.ManyToManyField(Unit, default=[])

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
