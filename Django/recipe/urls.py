from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "recipe"

router = DefaultRouter()
# router.register(
#     "recipe", views.RecipeListViewSet, basename="recipe"
# )  # RecipeListViewSet 등록
# router.register(
#     "detail_recipe", views.RecipeDetailViewSet, basename="detail_recipe"
# )  # RecipeDetailViewSet 등록

urlpatterns = [
    path("", include(router.urls)),
]
