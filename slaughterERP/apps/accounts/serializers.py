from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser, Role, Contact
from apps.product.models import Unit
from apps.product.serializers import UnitSerializer


class RoleSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    unit_ids = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Role
        fields = ['id', 'role_name', 'role_slug', 'units', 'unit_ids']
        read_only_fields = ['role_slug']

    def validate_role_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Role name cannot be empty."))
        if Role.objects.filter(role_name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Role name must be unique."))
        return value

    def create(self, validated_data):
        unit_ids = validated_data.pop('unit_ids', [])
        role = Role.objects.create(**validated_data)
        role.units.set(unit_ids)
        return role

    def update(self, instance, validated_data):
        unit_ids = validated_data.pop('unit_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if unit_ids is not None:
            instance.units.set(unit_ids)
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True, write_only=True)
    roles_detail = RoleSerializer(source='roles', many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'roles', 'roles_detail']
        read_only_fields = ['id']

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password('default-password')
        user.save()
        user.roles.set(roles)
        return user

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if roles is not None:
            instance.roles.set(roles)
        return instance


class ContactSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    unit_ids = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'slug', 'units', 'unit_ids']
        read_only_fields = ['slug']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(_("Contact name cannot be empty."))
        if Contact.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Contact name must be unique."))
        return value

    def create(self, validated_data):
        unit_ids = validated_data.pop('unit_ids', [])
        contact = Contact.objects.create(**validated_data)
        contact.units.set(unit_ids)
        return contact

    def update(self, instance, validated_data):
        unit_ids = validated_data.pop('unit_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if unit_ids is not None:
            instance.units.set(unit_ids)
        return instance
