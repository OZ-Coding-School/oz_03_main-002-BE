from app_user.models import App_User
from django.db import models
from ingredient.models import Ingredient


class Refrigerator(models.Model):
    user = models.ForeignKey(App_User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)


class RefrigeratorIngredientList(models.Model):
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    expiration_date = models.DateField()
