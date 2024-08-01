from django.conf import settings
from django.db import models


class IngreMajor(models.Model):
    name = models.CharField(max_length=255)


class IngreMiddle(models.Model):
    name = models.CharField(max_length=255)
    major = models.ForeignKey(IngreMajor, on_delete=models.CASCADE)


class IngreSub(models.Model):
    name = models.CharField(max_length=255)
    middle = models.ForeignKey(IngreMiddle, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    major = models.ForeignKey(IngreMajor, on_delete=models.CASCADE)
    middle = models.ForeignKey(IngreMiddle, on_delete=models.CASCADE, null=True)
    sub = models.ForeignKey(IngreSub, on_delete=models.CASCADE, null=True)
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )


class CustomIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "ingredient")
