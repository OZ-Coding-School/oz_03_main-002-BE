from common.decorators import login_required_ajax
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Refrigerator
from .models import RefrigeratorIngredient
from .serializers import RefrigeratorIngredientSerializer
from .serializers import RefrigeratorSerializer


class RefrigeratorList(APIView):
    """
    냉장고 목록 조회 및 생성 API
    """

    @swagger_auto_schema(
        operation_summary="냉장고 목록 조회",
        operation_description="현재 사용자의 모든 냉장고 목록을 반환합니다. 냉장고 이름으로 검색이 가능합니다.",
        manual_parameters=[
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="냉장고 이름 검색어",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            200: openapi.Response("냉장고 목록", RefrigeratorSerializer(many=True)),
            401: "인증되지 않은 사용자",
        },
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def get(self, request):
        name = request.query_params.get("name")
        queryset = Refrigerator.objects.filter(user=request.user)
        if name:
            queryset = queryset.filter(name__icontains=name)
        serializer = RefrigeratorSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="새 냉장고 추가",
        operation_description="새로운 냉장고를 추가합니다. 냉장고 이름과 설명을 입력해야 합니다.",
        request_body=RefrigeratorSerializer,
        responses={201: RefrigeratorSerializer(), 400: "유효하지 않은 요청 데이터"},
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def post(self, request):
        serializer = RefrigeratorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RefrigeratorDetail(APIView):
    """
    냉장고 상세 정보 조회, 수정, 삭제 API
    """

    @swagger_auto_schema(
        operation_summary="냉장고 상세 정보 조회",
        operation_description="특정 냉장고의 상세 정보를 반환합니다. 냉장고 ID를 사용하여 조회합니다.",
        responses={200: RefrigeratorSerializer(), 404: "냉장고를 찾을 수 없습니다."},
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def get(self, request, pk):
        try:
            refrigerator = Refrigerator.objects.get(pk=pk, user=request.user)
        except Refrigerator.DoesNotExist:
            return Response(
                {"error": "냉장고를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RefrigeratorSerializer(refrigerator)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="냉장고 정보 수정 (PUT)",
        operation_description="기존 냉장고의 정보를 전체 수정합니다. 냉장고 ID를 사용하여 수정할 냉장고를 선택합니다.",
        request_body=RefrigeratorSerializer,
        responses={
            200: RefrigeratorSerializer(),
            400: "유효하지 않은 요청 데이터",
            404: "냉장고를 찾을 수 없습니다.",
        },
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def put(self, request, pk):
        try:
            refrigerator = Refrigerator.objects.get(pk=pk, user=request.user)
        except Refrigerator.DoesNotExist:
            return Response(
                {"error": "냉장고를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RefrigeratorSerializer(refrigerator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="냉장고 정보 수정 (PATCH)",
        operation_description="기존 냉장고의 정보를 부분적으로 수정합니다. 냉장고 ID를 사용하여 수정할 냉장고를 선택합니다.",
        request_body=RefrigeratorSerializer,
        responses={
            200: RefrigeratorSerializer(),
            400: "유효하지 않은 요청 데이터",
            404: "냉장고를 찾을 수 없습니다.",
        },
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def patch(self, request, pk):
        try:
            refrigerator = Refrigerator.objects.get(pk=pk, user=request.user)
        except Refrigerator.DoesNotExist:
            return Response(
                {"error": "냉장고를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RefrigeratorSerializer(
            refrigerator, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="냉장고 삭제",
        operation_description="특정 냉장고를 삭제합니다. 냉장고 ID를 사용하여 삭제할 냉장고를 선택합니다.",
        responses={
            204: "냉장고가 성공적으로 삭제되었습니다.",
            404: "냉장고를 찾을 수 없습니다.",
        },
        tags=["Refrigerator"],
    )
    @login_required_ajax
    def delete(self, request, pk):
        try:
            refrigerator = Refrigerator.objects.get(pk=pk, user=request.user)
        except Refrigerator.DoesNotExist:
            return Response(
                {"error": "냉장고를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        refrigerator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RefrigeratorIngredientList(APIView):
    """
    냉장고 내 식재료 목록 조회 API
    """

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
