from django.urls import path

from .views import CustomIngredientCreateView
from .views import CustomIngredientDeleteView
from .views import CustomIngredientUpdateView
from .views import IngredientCreateView
from .views import IngredientDeleteView
from .views import IngredientDetailView
from .views import IngredientListView
from .views import IngredientUpdateView
from .views import IngreMajorListView
from .views import IngreMiddleListView
from .views import IngreSubListView
from .views import RefrigeratorIngredientAddView
from .views import RefrigeratorIngredientList

urlpatterns = [
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path(
        "ingredients/<int:pk>/",
        IngredientDetailView.as_view(),
        name="ingredient-detail",
    ),
    path(
        "ingredients/create/", IngredientCreateView.as_view(), name="ingredient-create"
    ),
    path(
        "ingredients/update/<int:pk>/",
        IngredientUpdateView.as_view(),
        name="ingredient-update",
    ),
    path(
        "ingredients/delete/<int:pk>/",
        IngredientDeleteView.as_view(),
        name="ingredient-delete",
    ),
    path(
        "custom-ingredients/create/",
        CustomIngredientCreateView.as_view(),
        name="custom-ingredient-create",
    ),
    path(
        "custom-ingredients/update/<int:pk>/",
        CustomIngredientUpdateView.as_view(),
        name="custom-ingredient-update",
    ),
    path(
        "custom-ingredients/delete/<int:pk>/",
        CustomIngredientDeleteView.as_view(),
        name="custom-ingredient-delete",
    ),
    path(
        "refrigerator-ingredients/add/",
        RefrigeratorIngredientAddView.as_view(),
        name="refrigerator-ingredient-add",
    ),
    path(
        "refrigerator-ingredients/<int:pk>/",
        RefrigeratorIngredientList.as_view(),
        name="refrigerator-ingredient-list",
    ),
    path(
        "categories/majors/", IngreMajorListView.as_view(), name="ingredient-major-list"
    ),
    path(
        "categories/middles/",
        IngreMiddleListView.as_view(),
        name="ingredient-middle-list",
    ),
    path("categories/subs/", IngreSubListView.as_view(), name="ingredient-sub-list"),
]
