from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import CustomUser
from validators import validate_names, validate_password
from django.core.validators import validate_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "middle_name", "last_name", "email", "password")

    def create(self, validated_data):
        model_class = self.Meta.model
        try:
            return model_class.create(**validated_data)
        except ValueError as ve:
            raise ValueError(ve)

    def update(self, instance, validated_data):
        model_class = self.Meta.model
        model_class.update(**validated_data)

    def validate(self, attrs):
        try:
            validate_names(attrs["first_name"])
            validate_names(attrs["last_name"])
            validate_names(attrs["middle_name"])
            validate_password(attrs["password"])
            validate_email(attrs["email"])
            return attrs
        except ValidationError as ve:
            raise serializers.ValidationError(ve)
