from rest_framework import serializers

from apps.core.models import ViewsRoles


class ViewsRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewsRoles
        fields = '__all__'
