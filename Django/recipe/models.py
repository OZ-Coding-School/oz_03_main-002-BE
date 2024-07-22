from django.db import models

from app_user.models import App_User
from ingredient.models import Ingredient


class CookingNameList(models.Model):
    name = models.CharField(max_length=255)


class CookingMethod(models.Model):
    name = models.CharField(max_length=255)


class CookingSituation(models.Model):
    name = models.CharField(max_length=255)


class CookingMainIngre(models.Model):
    name = models.CharField(max_length=255)


class CookingType(models.Model):
    name = models.CharField(max_length=255)


class RecipeDifficulty(models.TextChoices):
    EASY = "EASY", ("Easy")
    MEDIUM = "MEDIUM", ("Medium")
    HARD = "HARD", ("Hard")


class CookingAttribute(models.Model):
    name = models.ForeignKey(CookingNameList, on_delete=models.CASCADE, unique=True)
    method = models.ForeignKey(CookingMethod, on_delete=models.CASCADE, unique=True)
    situation = models.ForeignKey(CookingSituation, on_delete=models.CASCADE, unique=True)
    main_ingre = models.ForeignKey(CookingMainIngre, on_delete=models.CASCADE, unique=True)
    type = models.ForeignKey(CookingType, on_delete=models.CASCADE, unique=True)


class Recipe(models.Model):
    url = models.URLField()
    recipe_name = models.TextField()
    nick_name = models.ForeignKey(App_User, on_delete=models.CASCADE)
    recommend_num = models.PositiveIntegerField(default=0)
    recipe_intro = models.TextField(blank=True)
    eat_people = models.PositiveSmallIntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=RecipeDifficulty.choices, default=RecipeDifficulty.EASY)
    cooking_time = models.PositiveIntegerField(default=0)
    thumbnail_url = models.URLField(blank=True)
    attribute = models.OneToOneField(CookingAttribute, on_delete=models.CASCADE, unique=True)


class RecipeIngredientList(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class DetailRecipe(models.Model):
    img_url = models.URLField(blank=True)
    recipe_text = models.TextField()
    tip = models.TextField()
    step = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
