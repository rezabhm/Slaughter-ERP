from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Contact
from apps.core.models.ownership import City
from apps.product.models import ProductCategory


class Driver(models.Model):
    """
    Represents a driver with associated contacts.
    Links to Contact model via ManyToMany relationship.
    """
    contacts = models.ManyToManyField(
        Contact,
        blank=True,
        related_name="drivers",
        verbose_name=_("Contacts"),
        help_text=_("Contacts associated with this driver.")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        editable=False,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the driver.")
    )

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")
        ordering = ['slug']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def clean(self):
        """Validate driver data before saving."""
        if not self.contacts.exists() and not self.slug:
            raise ValidationError(_("At least one contact is required to generate a slug."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug from the first contact's name if not set.
        Ensures slug uniqueness and handles validation.
        """
        if not self.slug and self.contacts.exists():
            first_contact = self.contacts.first()
            self.slug = slugify(first_contact.name)
            base_slug = self.slug
            counter = 1
            while Driver.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the slug for string representation."""
        return self.slug


class Car(models.Model):
    """
    Represents a car with a license plate and associations to city, product category, and driver.
    """
    prefix_number = models.IntegerField(
        default=11,
        verbose_name=_("Prefix Number"),
        help_text=_("Prefix number of the license plate.")
    )
    alphabet = models.CharField(
        max_length=2,
        default='ط',
        verbose_name=_("Alphabet"),
        help_text=_("Alphabet part of the license plate.")
    )
    postfix_number = models.IntegerField(
        default=111,
        verbose_name=_("Postfix Number"),
        help_text=_("Postfix number of the license plate.")
    )
    city_code = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name=_("City Code"),
        help_text=_("City associated with the car's license plate.")
    )
    has_refrigerator = models.BooleanField(
        default=False,
        verbose_name=_("Has Refrigerator"),
        help_text=_("Indicates if the car has a refrigerator.")
    )
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name=_("Product Category"),
        help_text=_("Product category associated with the car.")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        editable=False,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the car.")
    )
    repetitive = models.BooleanField(
        default=False,
        verbose_name=_("Repetitive"),
        help_text=_("Indicates if the car is used for repetitive tasks.")
    )
    driver = models.OneToOneField(
        Driver,
        on_delete=models.CASCADE,
        related_name="car",
        verbose_name=_("Driver"),
        help_text=_("Driver assigned to this car.")
    )

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        ordering = ['prefix_number', 'alphabet', 'postfix_number']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['prefix_number', 'alphabet', 'postfix_number']),
        ]

    def clean(self):
        """Validate car data before saving."""
        if self.prefix_number < 0 or self.postfix_number < 0:
            raise ValidationError(_("License plate numbers cannot be negative."))
        if not self.alphabet.strip():
            raise ValidationError(_("Alphabet cannot be empty."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug from license plate details if not set.
        Ensures slug uniqueness and handles validation.
        """
        if not self.slug:
            plate = f"{self.prefix_number}{self.alphabet}{self.postfix_number}{self.city_code.car_code}"
            self.slug = slugify(plate)
            base_slug = self.slug
            counter = 1
            while Car.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the license plate representation."""
        return f"{self.prefix_number}{self.alphabet}{self.postfix_number}/{self.city_code.car_code}"