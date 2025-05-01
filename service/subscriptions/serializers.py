from rest_framework import serializers
from .models import Tariff, UserSubscription


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ["id", "tariff", "start_date", "end_date"]

    def validate(self, attrs):
        user = self.context["request"].user
        if UserSubscription.objects.filter(user=user, is_active=True).exists():
            raise serializers.ValidationError("Подписка уже активна")
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
