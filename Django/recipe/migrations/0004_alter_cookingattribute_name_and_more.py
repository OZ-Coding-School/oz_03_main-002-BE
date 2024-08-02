# Generated by Django 5.0.7 on 2024-08-01 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0003_alter_cookingattribute_main_ingre_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cookingattribute",
            name="name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="recipe.cookingnamelist"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="cookingattribute",
            unique_together={("method", "situation", "main_ingre", "type")},
        ),
    ]
