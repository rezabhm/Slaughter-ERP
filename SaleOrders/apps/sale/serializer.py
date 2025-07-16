from apps.sale.documents import TruckLoading, LoadedProduct, LoadedProductItem
from utils.CustomSerializer.custom_serializer import CustomSerializer
from rest_framework import serializers

class TruckLoadingSerializer(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = '__all__'

class TruckLoadingSerializerPOST(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = ['car']

class FirstWeightingSerializer(CustomSerializer):
    first_weight = serializers.CharField(required=True)

    class Meta:
        model = TruckLoading
        fields = ['first_weight']

class LastWeightingSerializer(CustomSerializer):
    last_weight = serializers.CharField(required=True)

    class Meta:
        model = TruckLoading
        fields = ['last_weight']

class ExitSerializer(CustomSerializer):
    exit_date = serializers.CharField(required=True)

    class Meta:
        model = TruckLoading
        fields = ['exit_date']

class CancelSerializer(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = []

class LoadedProductSerializer(CustomSerializer):
    class Meta:
        model = LoadedProduct
        fields = '__all__'

class LoadedProductSerializerPOST(CustomSerializer):
    class Meta:
        model = LoadedProduct
        fields = ['product', 'price', 'car', 'is_weight_base']

class LoadedProductItemSerializer(CustomSerializer):
    class Meta:
        model = LoadedProductItem
        fields = '__all__'

class LoadedProductItemSerializerPOST(CustomSerializer):
    class Meta:
        model = LoadedProductItem
        fields = ['weight', 'number', 'loaded_product']