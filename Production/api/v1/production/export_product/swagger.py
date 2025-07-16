from apps.production.documents import ExportProduct
from utils.CustomSerializer.custom_serializer import CustomSerializer


class VerifySwagger(CustomSerializer):

    class Meta:
        model = ExportProduct
        fields = []
