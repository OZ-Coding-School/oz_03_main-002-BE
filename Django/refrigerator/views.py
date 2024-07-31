from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Refrigerator, RefrigeratorIngredient
from .serializers import RefrigeratorSerializer, RefrigeratorIngredientSerializer
from common.decorators import login_required_ajax

class RefrigeratorViewSet(viewsets.ModelViewSet):
    """
    냉장고 관련 API
    """
    serializer_class = RefrigeratorSerializer
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Refrigerator.objects.none()  # 빈 쿼리셋 반환
        return Refrigerator.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="냉장고 목록 조회",
        operation_description="현재 사용자의 모든 냉장고 목록을 반환합니다.",
        responses={200: RefrigeratorSerializer(many=True)}
    )
    @login_required_ajax
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="냉장고 상세 정보 조회",
        operation_description="특정 냉장고의 상세 정보를 반환합니다.",
        responses={
            200: RefrigeratorSerializer(),
            404: "냉장고를 찾을 수 없습니다."
        }
    )
    @login_required_ajax
    def retrieve(self, request, pk=None):
        try:
            refrigerator = self.get_queryset().get(pk=pk)
        except Refrigerator.DoesNotExist:
            return Response({"error": "냉장고를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(refrigerator)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="새 냉장고 추가",
        operation_description="새로운 냉장고를 추가합니다.",
        request_body=RefrigeratorSerializer,
        responses={201: RefrigeratorSerializer()}
    )
    @login_required_ajax
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="냉장고 정보 수정",
        operation_description="기존 냉장고의 정보를 수정합니다.",
        request_body=RefrigeratorSerializer,
        responses={
            200: RefrigeratorSerializer(),
            404: "냉장고를 찾을 수 없습니다."
        }
    )
    @login_required_ajax
    def update(self, request, pk=None):
        try:
            refrigerator = self.get_queryset().get(pk=pk)
        except Refrigerator.DoesNotExist:
            return Response({"error": "냉장고를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(refrigerator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="냉장고 삭제",
        operation_description="특정 냉장고를 삭제합니다.",
        responses={
            204: "냉장고가 성공적으로 삭제되었습니다.",
            404: "냉장고를 찾을 수 없습니다."
        }
    )
    @login_required_ajax
    def destroy(self, request, pk=None):
        try:
            refrigerator = self.get_queryset().get(pk=pk)
        except Refrigerator.DoesNotExist:
            return Response({"error": "냉장고를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        refrigerator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="냉장고 내 식재료 목록 조회",
        operation_description="특정 냉장고 내의 모든 식재료 목록을 반환합니다.",
        responses={
            200: RefrigeratorIngredientSerializer(many=True),
            404: "냉장고를 찾을 수 없습니다."
        }
    )
    @action(detail=True, methods=['get'])
    @login_required_ajax
    def ingredients(self, request, pk=None):
        try:
            refrigerator = self.get_queryset().get(pk=pk)
        except Refrigerator.DoesNotExist:
            return Response({"error": "냉장고를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        ingredients = RefrigeratorIngredient.objects.filter(refrigerator=refrigerator)
        serializer = RefrigeratorIngredientSerializer(ingredients, many=True)
        return Response(serializer.data)