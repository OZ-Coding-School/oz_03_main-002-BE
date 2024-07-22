from django.contrib import admin

from .models import (
    CookingAttribute,
    CookingMainIngre,
    CookingMethod,
    CookingNameList,
    CookingSituation,
    CookingType,
    DetailRecipe,
    Recipe,
    RecipeIngredientList,
)


class RecipeIngredientListInline(admin.TabularInline):
    model = RecipeIngredientList
    extra = 1


class DetailRecipeInline(admin.TabularInline):
    model = DetailRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientListInline, DetailRecipeInline]
    list_display = (
        "recipe_name",
        "nick_name",
        "recommend_num",
        "difficulty",
        "cooking_time",
    )
    list_filter = ("difficulty", "cooking_time")
    search_fields = ("recipe_name", "nick_name__username")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(CookingNameList)
admin.site.register(CookingMethod)
admin.site.register(CookingSituation)
admin.site.register(CookingMainIngre)
admin.site.register(CookingType)
admin.site.register(CookingAttribute)
