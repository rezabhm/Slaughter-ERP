from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.product.models import Unit, ProductCategory, Product


class UnitSerializer(serializers.ModelSerializer):
    """
    Serializer for the Unit model.
    """
    class Meta:
        model = Unit
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

    def validate_name(self, value):
        """Ensure unit name is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("Unit name cannot be empty."))
        if Unit.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Unit name must be unique."))
        return value


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductCategory model.
    """
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

    def validate_name(self, value):
        """Ensure category name is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("Category name cannot be empty."))
        if ProductCategory.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Category name must be unique."))
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model, including nested category and unit details.
    """
    category = ProductCategorySerializer(read_only=True)
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'category', 'units', 'slug']
        read_only_fields = ['slug']

    def validate_name(self, value):
        """Ensure product name is not empty."""
        if not value.strip():
            raise serializers.ValidationError(_("Product name cannot be empty."))
        return value

    def validate_code(self, value):
        """Ensure product code is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("Product code cannot be empty."))
        if Product.objects.filter(code=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Product code must be unique."))
        return value


class ProductCategoryWithProductsSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCategory with a limited set of related products.
    """
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'products']
        read_only_fields = ['slug']

    def get_products(self, obj):
        """
        Retrieve up to 5 related products for the category.
        """
        products = Product.objects.filter(category=obj).select_related('category')[:5]
        return ProductSerializer(products, many=True, read_only=True).data


class UnitWithProductsSerializer(serializers.ModelSerializer):
    """
    Serializer for Unit with a limited set of related products.
    """
    products = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'name', 'slug', 'products']
        read_only_fields = ['slug']

    def get_products(self, obj):
        """
        Retrieve up to 5 related products for the unit.
        """
        products = Product.objects.filter(units=obj).select_related('category')[:5]
        return ProductSerializer(products, many=True, read_only=True).data