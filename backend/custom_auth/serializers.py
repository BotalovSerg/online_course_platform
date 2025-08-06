from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "role",
            "password",
            "password_confirm",
        ]

    def validate(self, data: dict):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data: dict):
        validated_data.pop("password_confirm")
        user = CustomUser(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            patronymic=validated_data.get("patronymic"),
            role=validated_data.get("role"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "role",
            "password",
        ]

    def update(self, instance: CustomUser, validated_data: dict):
        password = validated_data.pop("password")

        if not password or not instance.check_password(password):
            raise serializers.ValidationError("Неверные пароль")

        instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
