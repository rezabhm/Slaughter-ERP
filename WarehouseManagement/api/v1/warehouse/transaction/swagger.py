from apps.warehouse.documents import Transaction
from utils.custom_serializer import CustomSerializer


class VerifySwagger(CustomSerializer):

    class Meta:
        model = Transaction
        fields = []
