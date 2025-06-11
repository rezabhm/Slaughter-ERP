from apps.buy.documents import ProductionOrder
from apps.core.documents import CheckStatus
from utils.CustomSerializer.custom_serializer import CustomSerializer


class VerifiedActionSwagger(CustomSerializer):
    class Meta:
        model = CheckStatus
        fields = ['status', 'description']


class ReceivedActionSwagger(CustomSerializer):
    class Meta:
        model = CheckStatus
        fields = ['status', 'description']


class FinishedActionSwagger(CustomSerializer):
    class Meta:
        model = CheckStatus
        fields = ['status', 'description']


class DoneActionSwagger(CustomSerializer):
    class Meta:
        model = ProductionOrder
        fields = ['status', 'description', 'weight', 'quality', 'price']


class CancelledActionSwagger(CustomSerializer):
    class Meta:
        model = CheckStatus
        fields = ['status', 'description']