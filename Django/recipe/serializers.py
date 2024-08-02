from ingredient.models import Ingredient
from rest_framework import serializers

from .models import CookingAttribute
from .models import CookingMainIngre
from .models import CookingMethod
from .models import CookingNameList
from .models import CookingSituation
from .models import CookingType
from .models import DetailRecipe
from .models import Recipe
from .models import RecipeIngredientList


class CookingNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingNameList
        fields = ["id", "name"]


class CookingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingMethod
        fields = ["id", "name"]


class CookingSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingSituation
        fields = ["id", "name"]


class CookingMainIngreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingMainIngre
        fields = ["id", "name"]


class CookingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingType
        fields = ["id", "name"]


class CookingAttributeSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(queryset=CookingNameList.objects.all())
    method = serializers.PrimaryKeyRelatedField(queryset=CookingMethod.objects.all())
    situation = serializers.PrimaryKeyRelatedField(
        queryset=CookingSituation.objects.all()
    )
    main_ingre = serializers.PrimaryKeyRelatedField(
        queryset=CookingMainIngre.objects.all()
    )
    type = serializers.PrimaryKeyRelatedField(queryset=CookingType.objects.all())

    class Meta:
        model = CookingAttribute
        fields = ["name", "method", "situation", "main_ingre", "type"]


class RecipeIngredientListSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source="ingredient.name", read_only=True)

    class Meta:
        model = RecipeIngredientList
        fields = ["ingredient_name", "quantity"]


class RecipeSerializer(serializers.ModelSerializer):
    nick_name = serializers.CharField(
        source="nick_name.nick_name"
    )  # nick_name.nick_name으로 수정
    attribute = CookingAttributeSerializer()
    ingredients = RecipeIngredientListSerializer(
        source="recipeingredientlist_set",
        many=True,
        read_only=True,
        required=False,  # ingredients 필드를 optional로 설정
    )

    class Meta:
        model = Recipe
        fields = [
            "id",
            "url",
            "recipe_name",
            "nick_name",
            "recommend_num",
            "recipe_intro",
            "eat_people",
            "difficulty",
            "cooking_time",
            "thumbnail_url",
            "attribute",
            "ingredients",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        attribute_data = validated_data.pop("attribute")
        ingredients_data = validated_data.pop("ingredients", [])

        # CookingNameList 객체 조회 또는 생성
        name, _ = CookingNameList.objects.get_or_create(name=attribute_data["name"])
        method, _ = CookingMethod.objects.get_or_create(name=attribute_data["method"])
        situation, _ = CookingSituation.objects.get_or_create(
            name=attribute_data["situation"]
        )
        main_ingre, _ = CookingMainIngre.objects.get_or_create(
            name=attribute_data["main_ingre"]
        )
        type, _ = CookingType.objects.get_or_create(name=attribute_data["type"])

        cooking_attribute = CookingAttribute.objects.create(
            name=name,
            method=method,
            situation=situation,
            main_ingre=main_ingre,
            type=type,
        )
        recipe = Recipe.objects.create(attribute=cooking_attribute, **validated_data)

        for ingredient_data in ingredients_data:
            ingredient_name = ingredient_data.pop("ingredient_name")
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            RecipeIngredientList.objects.create(
                recipe=recipe, ingredient=ingredient, **ingredient_data
            )

        return recipe


class DetailRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailRecipe
        fields = ["img_url", "recipe_text", "tip", "step"]
