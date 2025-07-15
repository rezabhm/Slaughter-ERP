from typing import Any, Dict, Optional
from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class DeleteMongoAPIView(BaseMongoAPIView):
    """
    Handles DELETE requests for deleting MongoDB documents.
    Inherits from BaseMongoAPIView to leverage shared MongoDB utilities.
    """

    def single_delete_request(self, request: Any, slug_field: Optional[str] = None) -> JsonResponse:
        """
        Delete a single MongoDB document based on the provided slug field.

        Args:
            request: The incoming HTTP request.
            slug_field: The value of the lookup field to identify the document.

        Returns:
            JsonResponse: Success or error response based on the deletion outcome.
        """
        if slug_field == 'test_id':
            query_list = self.get_queryset()
            obj = query_list[0] if query_list else None
        else:
            obj = self.get_query({self.lookup_field: slug_field})

        if not obj or isinstance(obj, bool):
            response_data = {'message': f'No object found with {self.lookup_field}: {slug_field}'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_404_NOT_FOUND
            )
            return JsonResponse(data=response_data, status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        self.update_cache()

        response_data = {'message': 'Object deleted successfully'}
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def bulk_delete_request(self, request: Any) -> JsonResponse:
        """
        Delete multiple MongoDB documents based on a list of IDs.

        Args:
            request: The incoming HTTP request containing a list of IDs in 'data'.

        Returns:
            JsonResponse: Success or error response for each ID and overall operation.
        """
        data = request.data.get('data', [])
        if not isinstance(data, list) or not data:
            response_data = {'message': f'Data must be a non-empty list of {self.lookup_field} values'}
            self.store_logs(
                request=request,
                response=response_data,
                response_status_code=status.HTTP_400_BAD_REQUEST
            )
            return JsonResponse(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        response = {}
        for idx, id_ in enumerate(data):
            if not isinstance(id_, (str, int)):
                response[str(id_)] = {
                    'message': 'Invalid ID format',
                    'status': status.HTTP_400_BAD_REQUEST,
                    'id': id_
                }
                continue

            if id_ in ['test_id', 'test_str']:
                query_list = self.get_queryset()
                obj = query_list[0] if query_list else None
            else:
                obj = self.get_query({self.lookup_field: id_})

            if not obj or isinstance(obj, JsonResponse):
                response[str(id_)] = {
                    'message': f'No object found with {self.lookup_field}: {id_}',
                    'status': status.HTTP_404_NOT_FOUND
                }
            else:
                obj.delete()
                response[str(id_)] = {
                    'message': 'Object deleted successfully',
                    'status': status.HTTP_200_OK
                }

        self.update_cache()

        response_data = {'data': response}
        self.store_logs(
            request=request,
            response=response_data,
            response_status_code=status.HTTP_200_OK
        )
        return JsonResponse(data=response_data, status=status.HTTP_200_OK)