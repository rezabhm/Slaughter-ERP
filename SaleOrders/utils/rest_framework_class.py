from rest_framework.views import APIView


class BaseAPIView(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)