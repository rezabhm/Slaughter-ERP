from apps.order.documents import Order, OrderItem
from utils.CustomSerializer.custom_serializer import CustomSerializer
from rest_framework import serializers

class OrderSerializer(CustomSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializerPOST(CustomSerializer):
    class Meta:
        model = Order
        fields = ['customer']


class AttachmentStatusSerializer(CustomSerializer):
    order_item_ids = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        model = Order
        fields = ['order_item_ids']

class VerifiedSerializer(CustomSerializer):
    class Meta:
        model = Order
        fields = []

class CancelledSerializer(CustomSerializer):
    class Meta:
        model = Order
        fields = []

class OrderItemSerializer(CustomSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemSerializerPOST(CustomSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'weight', 'number', 'order']