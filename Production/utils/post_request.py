from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import status

from utils.jwt_validator import CustomJWTAuthentication
from utils.request_permission import RoleBasedPermission


def update_obj(request, attribute, attribute_value, obj_id, obj):

    post_data = request.data[obj_id][attribute] if attribute_value['send_required'] else ''
    new_data = attribute_value['fun'](request, post_data)
    setattr(obj, attribute, new_data)


class CustomAPIView(GenericAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]

    '''
    
    # Attribute structure defining expected fields and transformation functions
    attribute = {
        'create_date': {
            'send_required': False,
            'fun': lambda req, param_post_data: param_post_data + 1
        },
        'create_user': {
            'send_required': True,
            'fun': lambda req, param_post_data: param_post_data + 33
        },
    }
    
    '''

    def post(self, request):
        """
        Handles single or bulk update based on `many` key in input data.

        Example for single update:
        {
            "id": 2145,
            "create_date": 1,
            "user": "reza"
        }

        Example for bulk update:
        {
            "many": true,
            "2145": {
                "create_date": 45,
                "user": "ali"
            },
            "1": {
                "create_date": 1,
                "user": "reza"
            }
        }
        """

        # Determine if this is a bulk update
        many = request.data.get('many', False)

        # Convert single update format to bulk-like format
        if not many:
            request.data = {str(request.data['id']): request.data}

        # Process each object update
        for obj_id in request.data.keys():
            if obj_id == "many":
                continue  # Skip the 'many' key

            obj = self.get_query(obj_id)

            if not obj:
                return JsonResponse(
                    {"message": f"Object with ID <{obj_id}> not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Validate required fields
            msg, data_status = self.check_user_data(request.data[obj_id], obj_id)
            if not data_status:
                return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)

            # Apply transformations and set attributes
            for attribute, attribute_value in self.attribute.items():
                try:

                    update_obj(request=request,
                               attribute=attribute, attribute_value=attribute_value,
                               obj_id=obj_id, obj=obj)

                except Exception as e:
                    return JsonResponse(
                        {"message": f"Invalid value or type for <{attribute}>."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            obj.save()

        return JsonResponse(
            {"message": "Request processed successfully."},
            status=status.HTTP_200_OK
        )

    def check_user_data(self, data, obj_id=None):
        """
        Check if all required fields are provided in data.
        """
        id_str = f" in <{obj_id}>" if obj_id else ""
        for key, value in self.attribute.items():
            if value['send_required'] and key not in data:
                return {"message": f"You must provide <{key}>{id_str}."}, False
        return {}, True

    def get_query(self, id_):
        """
        Get object from queryset by ID.
        """
        try:
            return self.get_queryset().get(id=id_)
        except Exception:
            return None
