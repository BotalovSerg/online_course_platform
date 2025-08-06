from rest_framework import serializers

from .models import AccessRolesRule, BusinessElement, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description"]


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ["id", "name", "description"]


class AccessRolesRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRolesRule
        fields = [
            "id",
            "role",
            "element",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        ]
