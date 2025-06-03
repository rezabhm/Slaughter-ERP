from apps.buy.documents import ProductionOrder
from utils.custom_serializer import CustomSerializer


class ProductionOrderSerializer(CustomSerializer):
    class Meta:
        model = ProductionOrder
        fields = '__all__'


class ProductionOrderSerializerPOST(CustomSerializer):
    class Meta:
        model = ProductionOrder
        fields = ['car', 'order_information', 'required_weight', 'required_number']


class StatusActionSerializer(CustomSerializer):
    class Meta:
        model = ProductionOrder
        fields = ['status', 'description']


class DoneActionSerializer(CustomSerializer):
    class Meta:
        model = ProductionOrder
        fields = ['status', 'description', 'weight', 'quality', 'price']
