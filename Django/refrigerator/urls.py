from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "refrigerator"

router = DefaultRouter()
# router.register(
#     "", views.RefrigeratorViewSet, basename="refrigerator"
# )  # RefrigeratorViewSet 등록
router.register(
    "",
    views.RefrigeratorViewSet,
    basename="refrigerator_",
)  # RefrigeratorViewSet 등록

urlpatterns = [
    path("", include(router.urls)),
]
