from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Contact


class City(models.Model):
    """
    Represents a city with a unique name, car code, and slug.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("City Name"),
        help_text=_("Unique name of the city.")
    )
    car_code = models.IntegerField(
        default=11,
        verbose_name=_("Car Code"),
        help_text=_("Unique car code for the city.")
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        editable=False,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the city.")
    )

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
        ]

    def clean(self):
        """Validate city data before saving."""
        if not self.name.strip():
            raise ValidationError(_("City name cannot be empty."))
        if self.car_code < 0:
            raise ValidationError(_("Car code cannot be negative."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug from name if not set.
        Ensures slug uniqueness and handles validation.
        """
        if not self.slug:
            self.slug = slugify(self.name)
            base_slug = self.slug
            counter = 1
            while City.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the city name for string representation."""
        return self.name


class Agriculture(models.Model):
    """
    Represents an agriculture entity tied to a city.
    """
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
        help_text=_("Name of the agriculture entity.")
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="agricultures",
        verbose_name=_("City"),
        help_text=_("City associated with this agriculture entity.")
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        editable=False,
        blank=True,
        null=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the agriculture entity.")
    )

    class Meta:
        verbose_name = _("Agriculture")
        verbose_name_plural = _("Agricultures")
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def clean(self):
        """Validate agriculture data before saving."""
        if not self.name.strip():
            raise ValidationError(_("Agriculture name cannot be empty."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug from name if not set.
        Ensures slug uniqueness and handles validation.
        """
        if not self.slug:
            self.slug = slugify(self.name)
            base_slug = self.slug
            counter = 1
            while Agriculture.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the agriculture name for string representation."""
        return self.name


class ProductOwner(models.Model):
    """
    Represents a product owner linked to a contact.
    """
    contact = models.ForeignKey(
        Contact,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="product_owners",
        verbose_name=_("Contact"),
        help_text=_("Contact associated with this product owner.")
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        editable=False,
        blank=True,
        null=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the product owner.")
    )

    class Meta:
        verbose_name = _("Product Owner")
        verbose_name_plural = _("Product Owners")
        ordering = ['contact__name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def clean(self):
        """Validate product owner data before saving."""
        if not self.contact:
            raise ValidationError(_("Contact cannot be null."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug from contact name if not set.
        Ensures slug uniqueness and handles validation.
        """
        if not self.slug:
            self.slug = slugify(self.contact.name)
            base_slug = self.slug
            counter = 1
            while ProductOwner.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the contact name for string representation."""
        return self.contact.name