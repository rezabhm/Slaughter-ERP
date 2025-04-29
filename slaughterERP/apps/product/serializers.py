from rest_framework import serializers

from apps.product.models import *


class UnitSerializers(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = '__all__'


class ProductCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
