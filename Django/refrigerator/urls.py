from django.urls import path

from .views import RefrigeratorDetail
from .views import RefrigeratorIngredientList
from .views import RefrigeratorList

urlpatterns = [
    path("refrigerator/", RefrigeratorList.as_view(), name="refrigerator-list"),
    path(
        "refrigerator/<int:pk>/",
        RefrigeratorDetail.as_view(),
        name="refrigerator-detail",
    ),
    path(
        "refrigerator/<int:pk>/ingredients/",
        RefrigeratorIngredientList.as_view(),
        name="refrigerator-ingredient-list",
    ),
]
