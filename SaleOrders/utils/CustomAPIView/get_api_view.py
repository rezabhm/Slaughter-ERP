from typing import Any, Dict, Optional
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class GetMongoAPIView(BaseMongoAPIView):
    """
    Handles GET requests for retrieving MongoDB documents.
    Inherits from BaseMongoAPIView to leverage shared MongoDB utilities.
    """

    def get(self, request: Any, slug_field: Optional[str] = None, *args, **kwargs) -> JsonResponse:
        """
        Route GET request to single or bulk document retrieval based on slug_field.

        Args:
            request: The incoming HTTP request.
            slug_field: The value of the lookup field for single document retrieval.

        Returns:
            JsonResponse: The response containing the requested document(s) or an error.
        """
        return self.single_get(request, slug_field) if slug_field else self.bulk_get(request)

    def single_get(self, request: Any, slug_field: Optional[str] = None, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a single MongoDB document by the lookup field.

        Args:
            request: The incoming HTTP request.
            slug_field: The value of the lookup field to identify the document.

        Returns:
            JsonResponse: The serialized document or an error response if not found.
        """
        if slug_field == 'test_id':
            query_list = self.get_queryset()
            obj = query_list[0] if query_list else None
        else:
            obj = self.get_query({self.lookup_field: str(slug_field)})

        if not obj or isinstance(obj, JsonResponse):
            response_data = {'message': f'No object found with {self.lookup_field}: {slug_field}'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_404_NOT_FOUND
            )
            return JsonResponse(data=response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class['GET'](obj)
        response_data = serializer.data
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def bulk_get(self, request: Any, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a filtered and ordered list of MongoDB documents, optionally using Elasticsearch.

        Args:
            request: The incoming HTTP request containing query parameters.

        Returns:
            JsonResponse: The serialized list of documents or an error response.
        """
        query_set = None
        if getattr(settings, 'ELASTICSEARCH_STATUS', False):
            for key, value in request.query_params.items():
                if key == 'q':
                    query_set = self.search_elasticsearch(value)
                    break

        if query_set is None:
            query_status, query_set = self.get_queryset_with_filters()
            if not query_status:
                self.store_logs(
                    request=request,
                    response=query_set,
                    response_status_code=status.HTTP_400_BAD_REQUEST
                )
                return JsonResponse(data=query_set, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class['GET'](query_set, many=True)
        response_data = {'data': serializer.data}
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)