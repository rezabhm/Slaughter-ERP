from rest_framework import serializers

from apps.poultry_cutting_production.documents import PoultryCuttingReturnProduct
from utils.custom_serializer import CustomSerializer


class VerifySwaggerSerializer(CustomSerializer):
    is_useful = serializers.BooleanField(default=True, required=False)
    is_repack = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = PoultryCuttingReturnProduct
        fields = ['is_useful', 'is_repack']