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

    def validate_name(self, value):
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

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Category name cannot be empty."))
        if ProductCategory.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Category name must be unique."))
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model using category and unit IDs instead of nested objects.
    """
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all())
    units = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'category', 'units', 'slug']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Product name cannot be empty."))
        return value

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Product code cannot be empty."))
        if Product.objects.filter(code=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Product code must be unique."))
        return value


class ProductCategoryWithProductsSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductCategory with limited products listed by nested serializer.
    """
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'products']

    def get_products(self, obj):
        products = Product.objects.filter(category=obj).select_related('category')[:5]
        return ProductSerializer(products, many=True, read_only=True).data


class UnitWithProductsSerializer(serializers.ModelSerializer):
    """
    Serializer for Unit with limited products listed by nested serializer.
    """
    products = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'name', 'slug', 'products']

    def get_products(self, obj):
        products = Product.objects.filter(units=obj).select_related('category')[:5]
        return ProductSerializer(products, many=True, read_only=True).data
