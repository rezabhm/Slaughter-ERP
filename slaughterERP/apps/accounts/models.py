from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.product.models import Unit


class Role(models.Model):
    """
    Represents a user role with associated units.
    Stores role details and links to Unit model via ManyToMany relationship.
    """
    role_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Role Name"),
        help_text=_("Human-readable name for the role.")
    )
    role_slug = models.SlugField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_("Role Slug"),
        help_text=_("URL-friendly identifier for the role.")
    )
    units = models.ManyToManyField(
        Unit,
        blank=True,
        related_name="roles",
        verbose_name=_("Units"),
        help_text=_("Units associated with this role.")
    )

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        ordering = ['role_name']

    def clean(self):
        """Validate role data before saving."""
        if not self.role_name.strip():
            raise ValidationError(_("Role name cannot be empty."))
        super().clean()

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate role_slug from role_name if not set.
        Ensures data consistency and handles slug uniqueness.
        """
        if not self.role_slug:
            self.role_slug = slugify(self.role_name)
            base_slug = self.role_slug
            counter = 1
            while Role.objects.filter(role_slug=self.role_slug).exclude(pk=self.pk).exists():
                self.role_slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the human-readable role name."""
        return self.role_name


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser with role associations.
    Links users to roles via ManyToMany relationship.
    """
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name="users",
        verbose_name=_("Roles"),
        help_text=_("Roles assigned to this user.")
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['username']

    def save(self, *args, **kwargs):
        """
        Override save to set a default password if none is provided.
        Ensures secure password handling and calls parent save method.
        """
        if not self.password:
            self.set_password('1234')
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the username for string representation."""
        return self.username


class Contact(models.Model):
    """
    Represents a contact with a unique name and associated units.
    Auto-generates a slug from the name for URL usage.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Unique name for the contact.")
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly identifier for the contact.")
    )
    units = models.ManyToManyField(
        Unit,
        blank=True,
        related_name="contacts",
        verbose_name=_("Units"),
        help_text=_("Units associated with this contact.")
    )

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['name']

    def clean(self):
        """Validate contact data before saving."""
        if not self.name.strip():
            raise ValidationError(_("Contact name cannot be empty."))
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
            while Contact.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return the contact name for string representation."""
        return self.name