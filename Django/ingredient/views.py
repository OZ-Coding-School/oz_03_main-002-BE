from common.decorators import custom_superuser_required
from common.decorators import login_required_ajax
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from refrigerator.models import Refrigerator
from refrigerator.models import RefrigeratorIngredient
from refrigerator.serializers import RefrigeratorIngredientSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomIngredient
from .models import Ingredient
from .models import IngreMajor
from .models import IngreMiddle
from .models import IngreSub
from .serializers import CustomIngredientSerializer
from .serializers import IngredientSerializer


class CustomAutoSchema(SwaggerAutoSchema):
    def get_serializer(self):
        serializer = super().get_serializer()
        if not self.view.request.user.is_superuser:
            if hasattr(serializer, "child"):  # ListSerializer인 경우
                if hasattr(serializer.child, "Meta") and hasattr(
                    serializer.child.Meta, "fields"
                ):
                    if "is_custom" in serializer.child.Meta.fields:
                        serializer.child.Meta.fields.remove("is_custom")
            elif hasattr(serializer, "Meta") and hasattr(serializer.Meta, "fields"):
                if "is_custom" in serializer.Meta.fields:
                    serializer.Meta.fields.remove("is_custom")
        return serializer


class IngredientListView(APIView):
    @swagger_auto_schema(
        operation_summary="식재료 목록 조회",
        operation_description="일반 식재료와 사용자의 커스텀 식재료 목록을 반환합니다.",
        responses={200: IngredientSerializer(many=True)},
        tags=["Ingredients"],
    )
    @login_required_ajax
    def get(self, request):
        ingredients = Ingredient.objects.filter(is_custom=False)
        custom_ingredients = Ingredient.objects.filter(
            is_custom=True, created_by=request.user
        )
        all_ingredients = ingredients | custom_ingredients
        serializer = IngredientSerializer(all_ingredients, many=True)
        return Response(serializer.data)


class IngredientDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="특정 식재료 정보 조회",
        operation_description="식재료 ID를 사용하여 특정 식재료의 상세 정보를 반환합니다.",
        responses={200: IngredientSerializer(), 404: "식재료를 찾을 수 없습니다."},
        tags=["Ingredients"],
    )
    @login_required_ajax
    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


class IngredientCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="식재료 추가",
        operation_description="새로운 식재료를 추가합니다. 관리자만 사용 가능합니다.",
        request_body=IngredientSerializer,
        responses={
            201: IngredientSerializer(),
            400: "잘못된 데이터",
        },
        tags=["Ingredients"],
        auto_schema=CustomAutoSchema,
    )
    @custom_superuser_required
    def post(self, request):
        serializer = IngredientSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientUpdateView(APIView):
    @swagger_auto_schema(
        operation_summary="식재료 정보 수정",
        operation_description="기존 식재료의 정보를 수정합니다. 관리자만 사용 가능합니다.",
        request_body=IngredientSerializer,
        responses={
            200: IngredientSerializer(),
            400: "잘못된 데이터",
            404: "식재료를 찾을 수 없습니다.",
        },
        tags=["Ingredients"],
    )
    @custom_superuser_required
    def put(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDeleteView(APIView):
    @swagger_auto_schema(
        operation_summary="식재료 삭제",
        operation_description="특정 식재료를 삭제합니다. 관리자만 사용 가능합니다.",
        responses={
            204: "식재료가 성공적으로 삭제되었습니다.",
            404: "식재료를 찾을 수 없습니다.",
        },
        tags=["Ingredients"],
    )
    @custom_superuser_required
    def delete(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomIngredientCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="커스텀 식재료 추가",
        operation_description="사용자의 커스텀 식재료를 추가합니다. (이름, major, middle, sub 필요)",
        request_body=IngredientSerializer,  # CustomIngredientSerializer 대신 IngredientSerializer 사용
        responses={
            201: IngredientSerializer(),
            400: "잘못된 데이터",
        },
        tags=["Custom Ingredients"],
    )
    @login_required_ajax
    def post(self, request):
        # is_custom 필드를 True로 설정하여 커스텀 식재료임을 나타냅니다.
        request.data["is_custom"] = True
        serializer = IngredientSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            ingredient = serializer.save()  # Ingredient 생성
            CustomIngredient.objects.create(
                user=request.user, ingredient=ingredient
            )  # CustomIngredient 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomIngredientUpdateView(APIView):
    @swagger_auto_schema(
        operation_summary="커스텀 식재료 수정",
        operation_description="사용자의 커스텀 식재료 정보를 수정합니다.",
        request_body=CustomIngredientSerializer,
        responses={
            200: CustomIngredientSerializer(),
            400: "잘못된 데이터",
            403: "권한 없음",
            404: "커스텀 식재료를 찾을 수 없습니다.",
        },
        tags=["Custom Ingredients"],
    )
    @login_required_ajax
    def put(self, request, pk):
        custom_ingredient = get_object_or_404(
            CustomIngredient, pk=pk, user=request.user
        )
        serializer = CustomIngredientSerializer(custom_ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomIngredientDeleteView(APIView):
    @swagger_auto_schema(
        operation_summary="커스텀 식재료 삭제",
        operation_description="사용자의 커스텀 식재료를 삭제합니다.",
        responses={
            204: "커스텀 식재료가 성공적으로 삭제되었습니다.",
            403: "권한 없음",
            404: "커스텀 식재료를 찾을 수 없습니다.",
        },
        tags=["Custom Ingredients"],
    )
    @login_required_ajax
    def delete(self, request, pk):
        custom_ingredient = get_object_or_404(
            CustomIngredient, pk=pk, user=request.user
        )
        custom_ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RefrigeratorIngredientAddView(APIView):
    @swagger_auto_schema(
        operation_summary="냉장고에 식재료 추가",
        operation_description="사용자의 냉장고에 식재료를 추가합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refrigerator", "ingredient", "expiration_date"],
            properties={
                "refrigerator": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="냉장고 ID"
                ),
                "ingredient": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="식재료 ID"
                ),
                "expiration_date": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="유통기한",
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="수량"
                ),
                "unit": openapi.Schema(type=openapi.TYPE_STRING, description="단위"),
            },
        ),
        responses={
            201: RefrigeratorIngredientSerializer(),
            400: "잘못된 데이터",
            404: "냉장고 또는 식재료를 찾을 수 없습니다.",
        },
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def post(self, request):
        refrigerator_id = request.data.get("refrigerator")
        ingredient_id = request.data.get("ingredient")
        expiration_date = request.data.get("expiration_date")
        quantity = request.data.get("quantity", 1)
        unit = request.data.get("unit", "개")

        try:
            refrigerator = Refrigerator.objects.get(
                id=refrigerator_id, user=request.user
            )
            ingredient = Ingredient.objects.get(id=ingredient_id)
        except (Refrigerator.DoesNotExist, Ingredient.DoesNotExist):
            return Response(
                {"detail": "냉장고 또는 식재료를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        refrigerator_ingredient = RefrigeratorIngredient.objects.create(
            refrigerator=refrigerator,
            ingredient=ingredient,
            expiration_date=expiration_date,
            quantity=quantity,
            unit=unit,
        )

        serializer = RefrigeratorIngredientSerializer(refrigerator_ingredient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RefrigeratorIngredientList(APIView):
    @swagger_auto_schema(
        operation_summary="냉장고 내 식재료 목록 조회",
        operation_description="특정 냉장고 내의 모든 식재료 목록을 반환합니다. 냉장고 ID를 사용하여 조회합니다.",
        responses={
            200: RefrigeratorIngredientSerializer(many=True),
            404: "냉장고를 찾을 수 없습니다.",
        },
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def get(self, request, pk=None):
        try:
            refrigerator = Refrigerator.objects.get(pk=pk, user=request.user)
        except Refrigerator.DoesNotExist:
            return Response(
                {"error": "냉장고를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        ingredients = RefrigeratorIngredient.objects.filter(refrigerator=refrigerator)
        serializer = RefrigeratorIngredientSerializer(ingredients, many=True)
        return Response(serializer.data)


class CustomIngredientListView(APIView):
    """
    사용자의 커스텀 식재료 목록을 조회하는 API 뷰
    """

    @swagger_auto_schema(
        operation_summary="커스텀 식재료 목록 조회",
        operation_description="로그인한 사용자의 커스텀 식재료 목록을 반환합니다.",
        responses={200: IngredientSerializer(many=True)},
        tags=["Custom Ingredients"],
    )
    @login_required_ajax
    def get(self, request):
        custom_ingredients = Ingredient.objects.filter(
            is_custom=True, created_by=request.user
        )
        serializer = IngredientSerializer(custom_ingredients, many=True)
        return Response(serializer.data)


class IngreMajorListView(APIView):
    """
    식재료 대분류 목록을 조회하는 API 뷰
    """

    @swagger_auto_schema(
        operation_summary="식재료 대분류 목록 조회",
        operation_description="대분류 목록을 반환합니다.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description="대분류 목록",
            )
        },
        tags=["Ingredient Categories"],
    )
    @login_required_ajax
    def get(self, request):
        majors = IngreMajor.objects.values("id", "name")  # id와 name을 함께 가져오기
        return Response(
            [{"id": major["id"], "name": major["name"]} for major in majors]
        )  # 딕셔너리 리스트 형태로 변환


class IngreMiddleListView(APIView):
    """
    식재료 중분류 목록을 조회하는 API 뷰
    """

    @swagger_auto_schema(
        operation_summary="식재료 중분류 목록 조회",
        operation_description="중분류 목록을 반환합니다.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description="중분류 목록",
            )
        },
        tags=["Ingredient Categories"],
    )
    @login_required_ajax
    def get(self, request):
        middles = IngreMiddle.objects.values("id", "name")
        return Response(
            [{"id": middle["id"], "name": middle["name"]} for middle in middles]
        )


class IngreSubListView(APIView):
    """
    식재료 소분류 목록을 조회하는 API 뷰
    """

    @swagger_auto_schema(
        operation_summary="식재료 소분류 목록 조회",
        operation_description="소분류 목록을 반환합니다.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description="소분류 목록",
            )
        },
        tags=["Ingredient Categories"],
    )
    @login_required_ajax
    def get(self, request):
        subs = IngreSub.objects.values("id", "name")
        return Response([{"id": sub["id"], "name": sub["name"]} for sub in subs])
