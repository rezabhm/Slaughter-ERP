from rest_framework import serializers
from apps.orders.documents import PurchaseOrder
from utils.CustomSerializer.custom_serializer import CustomSerializer


class VerifiedFinanceSwaggerSerializer(CustomSerializer):
    status = serializers.BooleanField(default=True)
    description = serializers.CharField(default='', allow_blank=True)

    class Meta:
        model = PurchaseOrder
        fields = ['status', 'description']


class ApprovedByPurchaserSwaggerSerializer(CustomSerializer):
    status = serializers.BooleanField(default=True)
    description = serializers.CharField(default='', allow_blank=True)
    estimated_price = serializers.IntegerField(required=True)
    planned_purchase_date = serializers.DateTimeField(required=True)

    class Meta:
        model = PurchaseOrder
        fields = ['status', 'description', 'estimated_price', 'planned_purchase_date']


class PurchasedSwaggerSerializer(CustomSerializer):
    status = serializers.BooleanField(default=True)
    description = serializers.CharField(default='', allow_blank=True)
    final_price = serializers.IntegerField(required=True)

    class Meta:
        model = PurchaseOrder
        fields = ['status', 'description', 'final_price']


class ReceivedSwaggerSerializer(CustomSerializer):
    status = serializers.BooleanField(default=True)
    description = serializers.CharField(default='', allow_blank=True)
    have_factor = serializers.BooleanField(required=True)

    class Meta:
        model = PurchaseOrder
        fields = ['status', 'description', 'have_factor']


class DoneSwaggerSerializer(CustomSerializer):
    status = serializers.BooleanField(default=True)
    description = serializers.CharField(default='', allow_blank=True)

    class Meta:
        model = PurchaseOrder
        fields = ['status', 'description']


class CancelledSwaggerSerializer(CustomSerializer):
    status = serializers.BooleanField(default=True)
    description = serializers.CharField(default='', allow_blank=True)

    class Meta:
        model = PurchaseOrder
        fields = ['status', 'description']