from django.contrib import admin

from .models import CookingAttribute
from .models import CookingMainIngre
from .models import CookingMethod
from .models import CookingNameList
from .models import CookingSituation
from .models import CookingType
from .models import DetailRecipe
from .models import Recipe
from .models import RecipeIngredientList


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
