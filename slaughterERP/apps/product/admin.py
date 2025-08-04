from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.product.models import Unit, ProductCategory, Product


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Unit model.
    Provides efficient management with search, filter, and display options.
    """
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug'),
            'description': _('Core details of the unit.')
        }),
    )

    def product_count(self, obj):
        """Display the number of products associated with the unit."""
        return obj.products.count()
    product_count.short_description = _('Product Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('products')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductCategory model.
    Provides a user-friendly interface for managing product categories.
    """
    list_display = ('name', 'slug', 'product_count')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug'),
            'description': _('Core details of the product category.')
        }),
    )

    def product_count(self, obj):
        """Display the number of products in the category."""
        return obj.products.count()
    product_count.short_description = _('Product Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('products')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    Provides comprehensive management with search, filter, and display options.
    """
    list_display = ('name', 'code', 'category', 'unit_count', 'slug')
    list_filter = ('category', 'units')
    search_fields = ('name', 'code', 'slug', 'category__name')
    readonly_fields = ('slug',)
    filter_horizontal = ('units',)
    list_select_related = ('category',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'slug'),
            'description': _('Core details of the product.')
        }),
        (_('Associations'), {
            'fields': ('category', 'units'),
            'description': _('Category and units associated with the product.')
        }),
    )

    def unit_count(self, obj):
        """Display the number of units associated with the product."""
        return obj.units.count()
    unit_count.short_description = _('Unit Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).select_related('category').prefetch_related('units')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)