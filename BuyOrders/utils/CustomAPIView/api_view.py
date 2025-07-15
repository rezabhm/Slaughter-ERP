
from utils.CustomAPIView.delete_api_view import DeleteMongoAPIView
from utils.CustomAPIView.get_api_view import GetMongoAPIView
from utils.CustomAPIView.patch_api_view import PatchMongoAPIView
from utils.CustomAPIView.post_api_view import PostMongoAPIView
from utils.CustomJWTAuthentication.jwt_validator import CustomJWTAuthentication
from utils.permissions import RoleBasedPermission
from utils.CustomAPIView.base_api_view import BaseMongoAPIView


class CustomAPIView(GetMongoAPIView, PostMongoAPIView, PatchMongoAPIView, DeleteMongoAPIView, BaseMongoAPIView):
    """Main API view that routes requests to appropriate method-specific handlers."""

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.documentation_serializer_class = {
            'single_get': '',
            'bulk_get': '',
            'single_post': '',
            'bulk_post': '',
            'single_patch': '',
            'bulk_patch': '',
            'single_delete': '',
            'bulk_delete': ''
        }

