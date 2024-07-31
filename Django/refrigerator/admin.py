from django.contrib import admin

from .models import Ingredient
from .models import Refrigerator
from .models import RefrigeratorIngredient


@admin.register(Refrigerator)
class RefrigeratorAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "brand", "purchase_year", "is_active", "created_at")
    list_filter = ("is_active", "brand")
    search_fields = ("name", "user__username", "brand")
    readonly_fields = ("created_at", "updated_at")


@admin.register(RefrigeratorIngredient)
class RefrigeratorIngredientAdmin(admin.ModelAdmin):
    list_display = ("refrigerator", "ingredient", "quantity", "unit", "expiration_date")
    list_filter = ("refrigerator", "ingredient")
    search_fields = ("refrigerator__name", "ingredient__name")
