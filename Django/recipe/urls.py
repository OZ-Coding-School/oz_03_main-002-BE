from django.urls import path

from .views import CookingMainIngreListView
from .views import CookingMethodListView
from .views import CookingNameListListView
from .views import CookingSituationListView
from .views import CookingTypeListView
from .views import DetailRecipeListView
from .views import RecipeCreateView
from .views import RecipeDetailView
from .views import RecipeFilterView
from .views import RecipeListView

urlpatterns = [
    path("recipes/", RecipeListView.as_view(), name="recipe-list"),
    path("recipes/create/", RecipeCreateView.as_view(), name="recipe-create"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipes/filter/", RecipeFilterView.as_view(), name="recipe-filter"),
    path(
        "recipes/<int:recipe_id>/detail_recipe/",
        DetailRecipeListView.as_view(),
        name="detail-recipe-list",
    ),
    path(
        "cooking_name_lists/",
        CookingNameListListView.as_view(),
        name="cooking-name-list",
    ),
    path(
        "cooking_methods/", CookingMethodListView.as_view(), name="cooking-method-list"
    ),
    path(
        "cooking_situations/",
        CookingSituationListView.as_view(),
        name="cooking-situation-list",
    ),
    path(
        "cooking_main_ingres/",
        CookingMainIngreListView.as_view(),
        name="cooking-main-ingre-list",
    ),
    path("cooking_types/", CookingTypeListView.as_view(), name="cooking-type-list"),
]
