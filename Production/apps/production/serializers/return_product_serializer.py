from apps.production.documents import ReturnProduct
from utils.CustomSerializer.custom_serializer import CustomSerializer


class ReturnProductSerializer(CustomSerializer):

    class Meta:
        model = ReturnProduct
        fields = '__all__'


class ReturnProductSerializerPOST(CustomSerializer):

    class Meta:
        model = ReturnProduct
        fields = ['receiver_delivery_unit', 'product', 'product_information', 'return_type']
