from rest_framework import serializers

from apps.accounts.models import *
from apps.product.serializers import UnitSerializer


class CustomUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'id']

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        role_list = []

        for role_id in representation['role']:

            role = Role.objects.get(id=role_id)
            role_serializer = RoleSerializers(data=[role], many=True)
            role_serializer.is_valid()

            role_list.append(role_serializer.data[0])

        representation['role'] = role_list

        return representation


class RoleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        unit_list = []
        for unit_id in representation['unit']:

            unit = Unit.objects.get(id=unit_id)
            unit_serializer = UnitSerializer(data=[unit], many=True)
            unit_serializer.is_valid()
            unit_list.append(unit_serializer.data[0])

        representation['unit'] = unit_list
        return representation


class ContactSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        unit_list = []
        for unit_id in representation['unit']:

            unit = Unit.objects.get(id=unit_id)
            unit_serializer = UnitSerializer(data=[unit], many=True)
            unit_serializer.is_valid()
            unit_list.append(unit_serializer.data[0])

        representation['unit'] = unit_list
        return representation