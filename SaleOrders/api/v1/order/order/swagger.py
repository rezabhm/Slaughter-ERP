from apps.core.documents import CheckStatus
from apps.order.documents import Order
from utils.custom_serializer import CustomSerializer


class OrderSwagger(CustomSerializer):
    class Meta:
        model = Order
        fields = []


class AttachmentStatusSwagger(CustomSerializer):
    class Meta:
        model = Order
        fields = ['car']


class VerifiedSwagger(CustomSerializer):
    class Meta:
        model = CheckStatus
        fields = ['status']


class CancelledSwagger(CustomSerializer):
    class Meta:
        model = Order
        fields = []