from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "ingredient"

router = DefaultRouter()
# router.register(
#     "ingredient", views.IngredientViewSet, basename="ingredient"
# )  # IngredientViewSet 등록

urlpatterns = [
    path("", include(router.urls)),
]
