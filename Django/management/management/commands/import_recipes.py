import json
import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from ingredient.models import Ingredient
from ingredient.models import IngreMajor
from recipe.models import CookingAttribute
from recipe.models import CookingMainIngre
from recipe.models import CookingMethod
from recipe.models import CookingNameList
from recipe.models import CookingSituation
from recipe.models import CookingType
from recipe.models import DetailRecipe
from recipe.models import Recipe
from recipe.models import RecipeDifficulty
from recipe.models import RecipeIngredientList

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Command(BaseCommand):
    help = "Import recipes from JSON file"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        json_file = options["json_file"]

        # JSON 데이터 로드
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.import_recipes(data)

    @transaction.atomic
    def import_recipes(self, data):
        for recipe_data in data.values():
            try:
                self.create_recipe(recipe_data)
            except Exception as e:
                logging.error(
                    f"Error inserting recipe {recipe_data.get('recipe_name', 'Unknown')}: {str(e)}"
                )

    def map_difficulty(self, difficulty):
        difficulty = difficulty.upper()
        if difficulty in ["초급", "EASY"]:
            return RecipeDifficulty.EASY
        elif difficulty in ["중급", "MEDIUM"]:
            return RecipeDifficulty.MEDIUM
        elif difficulty in ["고급", "HARD"]:
            return RecipeDifficulty.HARD
        else:
            return RecipeDifficulty.EASY  # 기본값

    def get_or_create(self, model, name):
        obj, created = model.objects.get_or_create(name=name)
        return obj

    def get_or_create_ingredient(self, ingre_name):
        ingredient = Ingredient.objects.filter(name=ingre_name).first()
        if ingredient:
            return ingredient
        else:
            # 기본 IngreMajor 생성 또는 가져오기
            default_major, _ = IngreMajor.objects.get_or_create(name="기타")
            return Ingredient.objects.create(
                name=ingre_name, major=default_major, is_custom=True
            )

    def create_recipe(self, recipe_data):
        # CookingAttribute 관련 객체 가져오기 또는 생성
        name = self.get_or_create(CookingNameList, recipe_data["cooking_name"])
        method = self.get_or_create(CookingMethod, recipe_data["cooking_method"])
        situation = self.get_or_create(CookingSituation, recipe_data["situation_type"])
        main_ingre = self.get_or_create(
            CookingMainIngre, recipe_data["main_ingredient_type"]
        )
        type_ = self.get_or_create(CookingType, recipe_data["cooking_type"])

        # CookingAttribute 생성
        attribute, _ = CookingAttribute.objects.get_or_create(
            name=name,
            method=method,
            situation=situation,
            main_ingre=main_ingre,
            type=type_,
        )

        # Recipe 생성
        recipe, created = Recipe.objects.get_or_create(
            url=recipe_data["URL"],
            defaults={
                "recipe_name": recipe_data["recipe_name"],
                "nick_name": recipe_data.get("nick_name", "None")[
                    :255
                ],  # max_length=255 제한
                "recommend_num": recipe_data["recommand_num"],
                "recipe_intro": recipe_data["recipe_intro"],
                "eat_people": int(recipe_data["eat_people"].replace("인분", "")),
                "difficulty": self.map_difficulty(recipe_data["difficulty"]),
                "cooking_time": int(recipe_data["cooking_time"][0]),
                "thumbnail_url": recipe_data.get("thumbnail_url", ""),
                "attribute": attribute,
            },
        )

        if not created:
            logging.info(f"Recipe already exists: {recipe_data['recipe_name']}")
            return

        # RecipeIngredientList 생성
        for ingre_name, quantity in recipe_data["ingre_list"].items():
            ingredient = self.get_or_create_ingredient(ingre_name)
            RecipeIngredientList.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity[:50],  # max_length=50 제한
            )

        # DetailRecipe 생성
        for step, detail in recipe_data["detail_recipes"].items():
            DetailRecipe.objects.create(
                recipe=recipe,
                step=int(step),
                img_url=detail.get("img_url", ""),
                recipe_text=detail["recipe"],
                tip=detail.get("tip", ""),
            )

        logging.info(f"Successfully inserted recipe: {recipe_data['recipe_name']}")
