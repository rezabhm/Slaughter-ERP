from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.core.models import ViewsRoles
from apps.core.serializer import ViewsRolesSerializer
from utils.CustomJWTAuthentication.jwt_validator import CustomJWTAuthentication
from utils.permissions import RoleBasedPermission


class ViewsRolesAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [RoleBasedPermission]
    serializer_class = ViewsRolesSerializer
    queryset = ViewsRoles.objects.all()
