from apps.log.documents import Logs
from utils.CustomSerializer.custom_serializer import CustomSerializer


class LogsSerializer(CustomSerializer):
    class Meta:
        model = Logs
        fields = '__all__'


class LogsSerializerPOST(CustomSerializer):
    class Meta:
        model = Logs
        fields = [

            'status_code',
            'response',
            'token_payload',
            'url',
            'request_body',
            'method',
            'request_header'

        ]
