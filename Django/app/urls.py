from common.decorators import superuser_required
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import (
    OpenAPISchemaGenerator,  # OpenAPISchemaGenerator import 추가
)
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

schema_view = get_schema_view(
    openapi.Info(
        title="냉똑이 API 문서",
        default_version="v1",
        description="API 설명",
        terms_of_service="https://",
        contact=openapi.Contact(email="joonho1366@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=OpenAPISchemaGenerator,  # OpenAPISchemaGenerator 사용
    authentication_classes=[],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("app_user.urls")),
    path("api/v1/", include("allauth.urls")),
    path("api/v1/refrigerator/", include("refrigerator.urls")),
    path("api/v1/ingredient/", include("ingredient.urls")),
    path("api/v1/recipe/", include("recipe.urls")),
    path(
        "swagger/",
        superuser_required(
            schema_view.with_ui("swagger", cache_timeout=0), login_url="/admin/login/"
        ),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        superuser_required(
            schema_view.with_ui("redoc", cache_timeout=0), login_url="/admin/login/"
        ),
        name="schema-redoc",
    ),
]
