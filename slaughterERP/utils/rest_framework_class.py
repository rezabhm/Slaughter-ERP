from rest_framework.views import APIView


class BaseAPIView(APIView):

    def dispatch(self, request, *args, **kwargs):
        # print('check request before ...')
        return super().dispatch(request, *args, **kwargs)