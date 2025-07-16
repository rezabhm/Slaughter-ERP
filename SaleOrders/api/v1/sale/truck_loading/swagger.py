from apps.sale.documents import TruckLoading
from utils.CustomSerializer.custom_serializer import CustomSerializer

class TruckLoadingSwagger(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = []

class FirstWeightingSwagger(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = ['first_weight']

class LastWeightingSwagger(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = ['last_weight']

class ExitSwagger(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = []

class CancelSwagger(CustomSerializer):
    class Meta:
        model = TruckLoading
        fields = []