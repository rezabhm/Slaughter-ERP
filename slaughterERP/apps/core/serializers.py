from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.serializers import ContactSerializer
from apps.core.models.ownership import City, Agriculture, ProductOwner
from apps.core.models.transportation import Driver, Car
from apps.product.serializers import ProductCategorySerializer


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'car_code', 'slug']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("City name cannot be empty."))
        if City.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("City name must be unique."))
        return value

    def validate_car_code(self, value):
        if value < 0:
            raise serializers.ValidationError(_("Car code cannot be negative."))
        return value


class AgricultureSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Agriculture
        fields = ['id', 'name', 'city', 'slug']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['city'] = CitySerializer(instance.city).data if instance.city else None
        return rep

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Agriculture name cannot be empty."))
        return value


class ProductOwnerSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=ContactSerializer.Meta.model.objects.all())

    class Meta:
        model = ProductOwner
        fields = ['id', 'contact', 'slug']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['contact'] = ContactSerializer(instance.contact).data if instance.contact else None
        return rep


class DriverSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(queryset=ContactSerializer.Meta.model.objects.all())

    class Meta:
        model = Driver
        fields = ['id', 'contact', 'slug']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['contact'] = ContactSerializer(instance.contact).data if instance.contact else None
        return rep


class CarSerializer(serializers.ModelSerializer):
    city_code = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    product_category = serializers.PrimaryKeyRelatedField(queryset=ProductCategorySerializer.Meta.model.objects.all())
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())

    class Meta:
        model = Car
        fields = [
            'id', 'prefix_number', 'alphabet', 'postfix_number', 'city_code',
            'has_refrigerator', 'product_category', 'slug', 'repetitive', 'driver'
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['city_code'] = CitySerializer(instance.city_code).data if instance.city_code else None
        rep['product_category'] = ProductCategorySerializer(instance.product_category).data if instance.product_category else None
        rep['driver'] = DriverSerializer(instance.driver).data if instance.driver else None
        return rep

    def validate(self, data):
        if data.get('prefix_number', 0) < 0 or data.get('postfix_number', 0) < 0:
            raise serializers.ValidationError(_("License plate numbers cannot be negative."))
        if not data.get('alphabet', '').strip():
            raise serializers.ValidationError(_("Alphabet cannot be empty."))
        return data