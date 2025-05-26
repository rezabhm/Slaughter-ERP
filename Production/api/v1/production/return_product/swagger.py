from apps.production.documents import ReturnProduct
from utils.custom_serializer import CustomSerializer


class VerifyReturnProductSwagger(CustomSerializer):

    class Meta:
        model = ReturnProduct
        fields = ['is_useful', 'is_repack']
