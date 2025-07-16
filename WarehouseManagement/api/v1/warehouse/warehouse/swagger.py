from apps.warehouse.documents import Warehouse
from utils.CustomSerializer.custom_serializer import CustomSerializer


class ChangeActivationStatusSwagger(CustomSerializer):

    class Meta:
        model = Warehouse
        fields = []
