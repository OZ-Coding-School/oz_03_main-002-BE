# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import mixins
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.routers import DefaultRouter

# # Create your views here.


# class IngredientViewSet(viewsets.ViewSet):
#     """
#     재료 정보 관련 API
#     """

#     @swagger_auto_schema(
#         tags=["Ingredient"],
#         operation_summary="재료 정보 추가",
#         operation_description="새로운 재료 정보를 추가합니다.",
#     )
#     @action(detail=False, methods=["post"], name="create_ingredient", url_path="create")
#     def create_ingredient(self, request):
#         """
#         재료 정보 추가
#         """
#         return Response({"message": "재료 정보 추가 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Ingredient"],
#         operation_summary="재료 정보 업데이트",
#         operation_description="기존 재료 정보를 업데이트합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["put"],
#         name="update_ingredient",
#         url_path="update/<int:pk>",
#     )
#     def update_ingredient(self, request, pk=None):
#         """
#         재료 정보 업데이트
#         """
#         return Response({"message": "재료 정보 업데이트 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Ingredient"],
#         operation_summary="재료 정보 삭제",
#         operation_description="기존 재료 정보를 삭제합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["delete"],
#         name="delete_ingredient",
#         url_path="delete/<int:pk>",
#     )
#     def delete_ingredient(self, request, pk=None):
#         """
#         재료 정보 삭제
#         """
#         return Response({"message": "재료 정보 삭제 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Ingredient"],
#         operation_summary="재료 정보 받아오기",
#         operation_description="기존 재료 정보를 가져옵니다.",
#     )
#     @action(
#         detail=True,
#         methods=["get"],
#         name="retrieve_ingredient",
#         url_path="retrieve/<int:pk>",
#     )
#     def retrieve_ingredient(self, request, pk=None):
#         """
#         재료 정보 받아오기
#         """
#         return Response({"message": "재료 정보 받아오기 API (미구현)"})
