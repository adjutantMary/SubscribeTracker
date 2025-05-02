from rest_framework import serializers
from .models import Order
from subscriptions.models import CustomUser


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ["id", "description", "created_at", "user_id"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        validated_data["user"] = CustomUser.objects.get(id=user_id)
        return super().create(validated_data)
