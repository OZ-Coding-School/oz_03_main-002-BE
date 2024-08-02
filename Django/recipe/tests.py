from django.urls import path

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
]
