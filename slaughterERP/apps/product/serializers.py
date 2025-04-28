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
