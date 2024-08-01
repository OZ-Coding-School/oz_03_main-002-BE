from refrigerator.models import Refrigerator
from refrigerator.models import RefrigeratorIngredient
from rest_framework import serializers

from .models import CustomIngredient
from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
        read_only_fields = ["created_by"]  # created_by 필드를 읽기 전용으로 설정

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user  # 현재 사용자 할당
        return super().create(validated_data)


class CustomIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomIngredient
        fields = "__all__"
