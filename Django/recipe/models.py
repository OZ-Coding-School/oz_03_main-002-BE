from app_user.models import App_User
from django.db import models
from ingredient.models import Ingredient


class CookingNameList(models.Model):
    name = models.CharField(max_length=255, unique=True)


class CookingMethod(models.Model):
    name = models.CharField(max_length=255, unique=True)


class CookingSituation(models.Model):
    name = models.CharField(max_length=255, unique=True)


class CookingMainIngre(models.Model):
    name = models.CharField(max_length=255, unique=True)


class CookingType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class RecipeDifficulty(models.TextChoices):
    EASY = "EASY", ("Easy")
    MEDIUM = "MEDIUM", ("Medium")
    HARD = "HARD", ("Hard")


class CookingAttribute(models.Model):
    name = models.ForeignKey(
        CookingNameList, on_delete=models.CASCADE
    )  # ForeignKey로 변경
    method = models.ForeignKey(
        CookingMethod, on_delete=models.CASCADE
    )  # ForeignKey로 변경
    situation = models.ForeignKey(
        CookingSituation, on_delete=models.CASCADE
    )  # ForeignKey로 변경
    main_ingre = models.ForeignKey(
        CookingMainIngre, on_delete=models.CASCADE
    )  # ForeignKey로 변경
    type = models.ForeignKey(CookingType, on_delete=models.CASCADE)  # ForeignKey로 변경


class Recipe(models.Model):
    url = models.URLField()
    recipe_name = models.TextField()
    nick_name = models.CharField(
        max_length=255, blank=True, null=True
    )  # ForeignKey에서 CharField로 변경
    recommend_num = models.PositiveIntegerField(default=0)
    recipe_intro = models.TextField(blank=True)
    eat_people = models.PositiveSmallIntegerField(default=1)
    difficulty = models.CharField(
        max_length=10, choices=RecipeDifficulty.choices, default=RecipeDifficulty.EASY
    )
    cooking_time = models.PositiveIntegerField(default=0)
    thumbnail_url = models.URLField(blank=True)
    attribute = models.OneToOneField(
        CookingAttribute, on_delete=models.CASCADE, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 레시피 생성 시간 추가
    updated_at = models.DateTimeField(auto_now=True)  # 레시피 수정 시간 추가


class RecipeIngredientList(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True)  # 재료 수량 추가 (선택 사항)


class DetailRecipe(models.Model):
    img_url = models.URLField(blank=True)
    recipe_text = models.TextField()
    tip = models.TextField()
    step = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
