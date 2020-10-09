from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        model_class = self.Meta.model
        try:
            return model_class.create(validated_data.get('user'), validated_data.get('book'))
        except ValueError as ve:
            raise ValueError(ve)

    def update(self, instance, validated_data):
        model_class = self.Meta.model
        model_class.update(**validated_data)
