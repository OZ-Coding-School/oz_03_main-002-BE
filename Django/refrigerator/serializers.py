from ingredient.models import Ingredient
from rest_framework import serializers

from .models import Refrigerator
from .models import RefrigeratorIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class RefrigeratorIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RefrigeratorIngredient
        fields = ["id", "ingredient", "quantity", "unit", "expiration_date"]


class RefrigeratorSerializer(serializers.ModelSerializer):
    ingredients = RefrigeratorIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Refrigerator
        fields = [
            "id",
            "name",
            "brand",
            "purchase_year",
            "is_active",
            "created_at",
            "updated_at",
            "ingredients",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        user = validated_data.pop("user")  # user 값을 꺼내고 validated_data에서 제거
        refrigerator = Refrigerator.objects.create(
            user=user, **validated_data
        )  # user 값을 명시적으로 전달
        return refrigerator
