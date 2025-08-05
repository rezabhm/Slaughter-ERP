from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Unit(models.Model):
    """
    Represents a unit of measurement or categorization for products.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Unique name for the unit.")
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the unit.")
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
        ]

    def clean(self):
        """Validate unit data before saving."""
        if not self.name.strip():
            raise ValidationError(_("Unit name cannot be empty."))
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
            while Unit.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the unit name for string representation."""
        return self.name


class ProductCategory(models.Model):
    """
    Represents a category for grouping products.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Unique name for the product category.")
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the product category.")
    )

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
        ]

    def clean(self):
        """Validate product category data before saving."""
        if not self.name.strip():
            raise ValidationError(_("Category name cannot be empty."))
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
            while ProductCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the category name for string representation."""
        return self.name


class Product(models.Model):
    """
    Represents a product with a name, code, category, and associated units.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Name of the product.")
    )
    code = models.CharField(
        max_length=120,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("Unique code for the product.")
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Category"),
        help_text=_("Category to which the product belongs.")
    )
    units = models.ManyToManyField(
        Unit,
        blank=True,
        related_name="products",
        verbose_name=_("Units"),
        help_text=_("Units associated with this product.")
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the product.")
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['code']),
        ]

    def clean(self):
        """Validate product data before saving."""
        if not self.name.strip():
            raise ValidationError(_("Product name cannot be empty."))
        if not self.code.strip():
            raise ValidationError(_("Product code cannot be empty."))
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
            while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the product name for string representation."""
        return self.name