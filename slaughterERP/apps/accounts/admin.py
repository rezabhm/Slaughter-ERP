from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Role, CustomUser, Contact


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Role model.
    Provides a user-friendly interface for managing roles with search, filter, and display options.
    """
    list_display = ('role_name', 'role_slug', 'unit_count')
    list_filter = ('units',)
    search_fields = ('role_name', 'role_slug')
    readonly_fields = ('role_slug',)
    filter_horizontal = ('units',)
    ordering = ('role_name',)
    fieldsets = (
        (None, {
            'fields': ('role_name', 'role_slug'),
            'description': _('Core details of the role.')
        }),
        (_('Associations'), {
            'fields': ('units',),
            'description': _('Units associated with this role.')
        }),
    )

    def unit_count(self, obj):
        """Display the number of units associated with the role."""
        return obj.units.count()
    unit_count.short_description = _('Unit Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('units')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    Extends UserAdmin to include role associations and custom display fields.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role_count')
    list_filter = ('is_staff', 'is_superuser', 'roles')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('roles',)
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
            'description': _('Core user credentials.')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email'),
            'description': _('Personal details of the user.')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': _('User permissions and group assignments.')
        }),
        (_('Associations'), {
            'fields': ('roles',),
            'description': _('Roles assigned to this user.')
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
            'description': _('Timestamps for user activity.')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
            'description': _('Fields required to create a new user.')
        }),
        (_('Associations'), {
            'fields': ('roles',),
            'description': _('Roles to assign to the new user.')
        }),
    )

    def role_count(self, obj):
        """Display the number of roles associated with the user."""
        return obj.roles.count()
    role_count.short_description = _('Role Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('roles')

    def save_model(self, request, obj, form, change):
        """Ensure validation and default password handling on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.
    Provides efficient management of contacts with search, filter, and display options.
    """
    list_display = ('name', 'slug', 'unit_count')
    list_filter = ('units',)
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)
    filter_horizontal = ('units',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug'),
            'description': _('Core details of the contact.')
        }),
        (_('Associations'), {
            'fields': ('units',),
            'description': _('Units associated with this contact.')
        }),
    )

    def unit_count(self, obj):
        """Display the number of units associated with the contact."""
        return obj.units.count()
    unit_count.short_description = _('Unit Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('units')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)