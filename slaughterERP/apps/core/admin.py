from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.models.ownership import City, Agriculture, ProductOwner
from apps.core.models.transportation import Driver, Car


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the City model.
    Provides efficient management with search, filter, and display options.
    """
    list_display = ('name', 'car_code', 'slug', 'agriculture_count')
    list_filter = ('car_code',)
    search_fields = ('name', 'slug', 'car_code')
    readonly_fields = ('slug',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'car_code', 'slug'),
            'description': _('Core details of the city.')
        }),
    )

    def agriculture_count(self, obj):
        """Display the number of agriculture entities associated with the city."""
        return obj.agricultures.count()
    agriculture_count.short_description = _('Agriculture Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('agricultures')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Agriculture)
class AgricultureAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Agriculture model.
    Provides a user-friendly interface for managing agriculture entities.
    """
    list_display = ('name', 'city', 'slug')
    list_filter = ('city',)
    search_fields = ('name', 'slug', 'city__name')
    readonly_fields = ('slug',)
    ordering = ('name',)
    list_select_related = ('city',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug'),
            'description': _('Core details of the agriculture entity.')
        }),
        (_('Associations'), {
            'fields': ('city',),
            'description': _('City associated with this agriculture entity.')
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).select_related('city')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(ProductOwner)
class ProductOwnerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ProductOwner model.
    Manages product owners with efficient search and display options.
    """
    list_display = ('contact', 'slug')
    list_filter = ('contact',)
    search_fields = ('contact__name', 'slug')
    readonly_fields = ('slug',)
    ordering = ('contact__name',)
    list_select_related = ('contact',)
    fieldsets = (
        (None, {
            'fields': ('contact', 'slug'),
            'description': _('Core details of the product owner.')
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).select_related('contact')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Driver model.
    Provides efficient management with search, filter, and display options.
    """
    list_display = ('slug', 'contact_count')
    list_filter = ('contacts',)
    search_fields = ('slug', 'contacts__name')
    readonly_fields = ('slug',)
    filter_horizontal = ('contacts',)
    ordering = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('slug',),
            'description': _('Core details of the driver.')
        }),
        (_('Associations'), {
            'fields': ('contacts',),
            'description': _('Contacts associated with this driver.')
        }),
    )

    def contact_count(self, obj):
        """Display the number of contacts associated with the driver."""
        return obj.contacts.count()
    contact_count.short_description = _('Contact Count')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).prefetch_related('contacts')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Car model.
    Provides a comprehensive interface for managing cars with license plate details.
    """
    list_display = ('license_plate', 'city_code', 'has_refrigerator', 'product_category', 'driver', 'repetitive')
    list_filter = ('city_code', 'has_refrigerator', 'product_category', 'repetitive')
    search_fields = ('slug', 'prefix_number', 'alphabet', 'postfix_number', 'city_code__name', 'driver__slug')
    readonly_fields = ('slug',)
    list_select_related = ('city_code', 'product_category', 'driver')
    ordering = ('prefix_number', 'alphabet', 'postfix_number')
    fieldsets = (
        (None, {
            'fields': ('prefix_number', 'alphabet', 'postfix_number', 'slug'),
            'description': _('Core details of the car, including license plate.')
        }),
        (_('Associations'), {
            'fields': ('city_code', 'product_category', 'driver'),
            'description': _('Related entities for the car.')
        }),
        (_('Attributes'), {
            'fields': ('has_refrigerator', 'repetitive'),
            'description': _('Additional attributes of the car.')
        }),
    )

    def license_plate(self, obj):
        """Display the formatted license plate."""
        return obj.__str__()
    license_plate.short_description = _('License Plate')

    def get_queryset(self, request):
        """Optimize queryset to reduce database queries."""
        return super().get_queryset(request).select_related('city_code', 'product_category', 'driver').prefetch_related('driver__contacts')

    def save_model(self, request, obj, form, change):
        """Ensure validation and slug generation on save."""
        obj.full_clean()
        super().save_model(request, obj, form, change)