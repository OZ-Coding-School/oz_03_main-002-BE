from app_user.models import App_User
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
    nick_name = serializers.PrimaryKeyRelatedField(
        queryset=App_User.objects.all()
    )  # 닉네임 필드 수정
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

        # CookingAttribute 생성
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

        # Recipe 생성 및 ingredients 연결
        recipe = Recipe.objects.create(attribute=cooking_attribute, **validated_data)
        for ingredient_data in ingredients_data:
            ingredient_name = ingredient_data["ingredient_name"]
            quantity = ingredient_data["quantity"]  # 수량 정보 추가
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            RecipeIngredientList.objects.create(
                recipe=recipe, ingredient=ingredient, quantity=quantity
            )

        return recipe

    def update(self, instance, validated_data):
        attribute_data = validated_data.pop("attribute", None)
        ingredients_data = validated_data.pop("ingredients", [])
        nick_name_data = validated_data.pop("nick_name", None)

        # 레시피 기본 정보 업데이트
        instance = super().update(instance, validated_data)

        # CookingAttribute 업데이트
        if attribute_data:
            name, _ = CookingNameList.objects.get_or_create(name=attribute_data["name"])
            method, _ = CookingMethod.objects.get_or_create(
                name=attribute_data["method"]
            )
            situation, _ = CookingSituation.objects.get_or_create(
                name=attribute_data["situation"]
            )
            main_ingre, _ = CookingMainIngre.objects.get_or_create(
                name=attribute_data["main_ingre"]
            )
            type, _ = CookingType.objects.get_or_create(name=attribute_data["type"])

            instance.attribute.name = name
            instance.attribute.method = method
            instance.attribute.situation = situation
            instance.attribute.main_ingre = main_ingre
            instance.attribute.type = type
            instance.attribute.save()

        # RecipeIngredientList 업데이트
        if ingredients_data:
            # 기존 RecipeIngredientList 객체 삭제
            RecipeIngredientList.objects.filter(recipe=instance).delete()

            # 새로운 RecipeIngredientList 객체 생성 및 저장
            for ingredient_data in ingredients_data:
                ingredient_name = ingredient_data.pop("ingredient_name")
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                RecipeIngredientList.objects.create(
                    recipe=instance, ingredient=ingredient, **ingredient_data
                )

        # nick_name 업데이트 (get_or_create 대신 get 사용)
        if nick_name_data:
            try:
                nick_name_user = App_User.objects.get(nick_name=nick_name_data)
            except App_User.DoesNotExist:
                # nick_name이 존재하지 않는 경우, 기존 사용자의 nick_name만 변경
                instance.nick_name.nick_name = nick_name_data
                instance.nick_name.save()
            else:
                # nick_name이 이미 존재하는 경우, 해당 사용자로 변경
                instance.nick_name = nick_name_user

        instance.save()
        return instance


class DetailRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailRecipe
        fields = ["img_url", "recipe_text", "tip", "step"]
