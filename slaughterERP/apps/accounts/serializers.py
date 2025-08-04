from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import CustomUser, Role, Contact
from apps.product.serializers import UnitSerializer


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Role model, including nested unit details.
    """
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'role_name', 'role_slug', 'units']
        read_only_fields = ['role_slug']

    def validate_role_name(self, value):
        """Ensure role_name is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("Role name cannot be empty."))
        if Role.objects.filter(role_name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Role name must be unique."))
        return value


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, including nested role details.
    """
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'roles']
        read_only_fields = ['id']

    def validate_username(self, value):
        """Ensure username is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("Username cannot be empty."))
        if CustomUser.objects.filter(username=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Username must be unique."))
        return value

    def validate_email(self, value):
        """Ensure email is unique if provided."""
        if value and CustomUser.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Email must be unique."))
        return value


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model, including nested unit details.
    """
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'slug', 'units']
        read_only_fields = ['slug']

    def validate_name(self, value):
        """Ensure name is not empty and unique."""
        if not value.strip():
            raise serializers.ValidationError(_("Contact name cannot be empty."))
        if Contact.objects.filter(name=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(_("Contact name must be unique."))
        return value