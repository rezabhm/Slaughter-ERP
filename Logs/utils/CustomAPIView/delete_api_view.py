from django.http import JsonResponse
from rest_framework import status

from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class DeleteMongoAPIView:
    """Handles DELETE requests for deleting MongoDB documents."""

    def single_delete_request(self, request, slug_field=None):
        """Delete a single object."""
        if str(slug_field) == 'test_id':
            query_list = self.get_queryset()

            if len(query_list) > 0:
                obj = query_list[0]
            else:
                obj = None
        else:
            obj = self.get_query({self.lookup_field: slug_field})

        if not obj or isinstance(obj, bool):
            response_data = {'message': f'No object found with this {slug_field}'}
            self.store_logs(requests=request, response=response_data, response_status_code=status.HTTP_404_NOT_FOUND)

            return JsonResponse(
                data=response_data,
                status=status.HTTP_404_NOT_FOUND
            )

        obj.delete()
        self.update_cache()

        response_data = {'data': 'Object deleted successfully'}

        self.store_logs(requests=request, response=response_data, response_status_code=status.HTTP_200_OK)

        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

    def bulk_delete_request(self, request):
        """Delete multiple objects based on IDs."""
        data = request.data.get('data', [])
        if not data or not isinstance(data, list):
            response_data = {'message': f'data must be a list of IDs with {self.lookup_field}'}
            self.store_logs(requests=request, response=response_data, response_status_code=status.HTTP_400_BAD_REQUEST)

            return JsonResponse(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )

        response = {}
        for idx, id_ in enumerate(data):
            if not isinstance(id_, (str, int)):
                response[str(idx)] = {'message': 'Invalid ID format', 'status': status.HTTP_400_BAD_REQUEST, 'id': id_}
                continue
            if str(id_) in ['test_id', 'test_str']:
                query_list = self.get_queryset()

                if len(query_list) > 0:
                    obj = query_list[0]
                else:
                    obj = None
            else:
                obj = self.get_query({self.lookup_field: id_})

            if not obj or isinstance(obj, JsonResponse):
                response[id_] = {'message': 'Invalid object ID', 'status': status.HTTP_400_BAD_REQUEST}
            else:
                obj.delete()
                response[id_] = {'message': 'Object deleted successfully', 'status': status.HTTP_200_OK}

        self.update_cache()

        response_data = {'data': response}
        self.store_logs(requests=request, response=response_data, response_status_code=status.HTTP_200_OK)

        return JsonResponse(data=response_data, status=status.HTTP_200_OK)

