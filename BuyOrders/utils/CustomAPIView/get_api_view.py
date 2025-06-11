from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class GetMongoAPIView:
    """Handles GET requests for retrieving MongoDB documents."""

    def get(self, request, slug_field=None, *args, **kwargs):
        """Route GET request to single or bulk retrieval."""
        return self.single_get(slug_field) if slug_field else self.bulk_get()

    def single_get(self, request, slug_field=None, *args, **kwargs):
        """Retrieve a single document by lookup field."""
        obj = self.get_query({self.lookup_field: str(slug_field)})
        if not obj:
            return JsonResponse(
                data={'message': f'No object found with {self.lookup_field} = "{slug_field}".'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class['GET'](obj)
        return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)

    def bulk_get(self, request, *args, **kwargs):
        """Retrieve a filtered and ordered list of documents."""
        query_status, query_set = self.get_queryset_with_filters()
        if not query_status:
            return JsonResponse(data=query_set, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class['GET'](query_set, many=True)
        return JsonResponse(data={'data': serializer.data}, status=status.HTTP_200_OK)

