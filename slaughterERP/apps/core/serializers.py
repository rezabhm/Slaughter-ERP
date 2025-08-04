from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.serializers import ContactSerializer
from apps.core.models.ownership import City, Agriculture, ProductOwner
from apps.core.models.transportation import Driver, Car
from apps.product.serializers import ProductCategorySerializer


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for the City model.
    """
    class Meta:
        model = City
        fields = ['id', 'name', 'car_code', 'slug']
        read_only_fields = ['slug']

    def validate_name(self, value):
        """Ensure city name is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("City name cannot be empty."))
        if City.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("City name must be unique."))
        return value

    def validate_car_code(self, value):
        """Ensure car code is non-negative."""
        if value < 0:
            raise serializers.ValidationError(_("Car code cannot be negative."))
        return value


class AgricultureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Agriculture model, including nested city details.
    """
    city = CitySerializer(read_only=True)

    class Meta:
        model = Agriculture
        fields = ['id', 'name', 'city', 'slug']
        read_only_fields = ['slug']

    def validate_name(self, value):
        """Ensure agriculture name is not empty."""
        if not value.strip():
            raise serializers.ValidationError(_("Agriculture name cannot be empty."))
        return value


class ProductOwnerSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductOwner model, including nested contact details.
    """
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = ProductOwner
        fields = ['id', 'contact', 'slug']
        read_only_fields = ['slug']


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for the Driver model, including nested contact details.
    """
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'contacts', 'slug']
        read_only_fields = ['slug']


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for the Car model, including nested city, product category, and driver details.
    """
    city_code = CitySerializer(read_only=True)
    product_category = ProductCategorySerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'prefix_number', 'alphabet', 'postfix_number', 'city_code',
            'has_refrigerator', 'product_category', 'slug', 'repetitive', 'driver'
        ]
        read_only_fields = ['slug']

    def validate(self, data):
        """Validate car data."""
        if data.get('prefix_number', 0) < 0 or data.get('postfix_number', 0) < 0:
            raise serializers.ValidationError(_("License plate numbers cannot be negative."))
        if not data.get('alphabet', '').strip():
            raise serializers.ValidationError(_("Alphabet cannot be empty."))
        return data