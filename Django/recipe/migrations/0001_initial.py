# Generated by Django 5.0.7 on 2024-07-24 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("app_user", "0001_initial"),
        ("ingredient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CookingMainIngre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="CookingMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="CookingNameList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="CookingSituation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="CookingType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="CookingAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "main_ingre",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.cookingmainingre",
                    ),
                ),
                (
                    "method",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.cookingmethod",
                    ),
                ),
                (
                    "name",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.cookingnamelist",
                    ),
                ),
                (
                    "situation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.cookingsituation",
                    ),
                ),
                (
                    "type",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.cookingtype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                ("recipe_name", models.TextField()),
                ("recommend_num", models.PositiveIntegerField(default=0)),
                ("recipe_intro", models.TextField(blank=True)),
                ("eat_people", models.PositiveSmallIntegerField(default=1)),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("EASY", "Easy"),
                            ("MEDIUM", "Medium"),
                            ("HARD", "Hard"),
                        ],
                        default="EASY",
                        max_length=10,
                    ),
                ),
                ("cooking_time", models.PositiveIntegerField(default=0)),
                ("thumbnail_url", models.URLField(blank=True)),
                (
                    "attribute",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.cookingattribute",
                    ),
                ),
                (
                    "nick_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_user.app_user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DetailRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("img_url", models.URLField(blank=True)),
                ("recipe_text", models.TextField()),
                ("tip", models.TextField()),
                ("step", models.PositiveSmallIntegerField()),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeIngredientList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ingredient.ingredient",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
                    ),
                ),
            ],
        ),
    ]
