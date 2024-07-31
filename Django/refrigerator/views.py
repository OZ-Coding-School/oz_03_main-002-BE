# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import mixins
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.routers import DefaultRouter


# # Create your views here.
# class RefrigeratorViewSet(viewsets.ViewSet):
#     """
#     냉장고 관련 API
#     """

#     @swagger_auto_schema(
#         tags=["Refrigerator"],
#         operation_summary="새로운 냉장고 추가",
#         operation_description="새로운 냉장고를 추가합니다.",
#     )
#     @action(
#         detail=False, methods=["post"], name="create_refrigerator", url_path="create"
#     )
#     def create_refrigerator(self, request):
#         """
#         새로운 냉장고 추가
#         """
#         return Response({"message": "새로운 냉장고 추가 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Refrigerator"],
#         operation_summary="기존 냉장고 이름 수정",
#         operation_description="기존 냉장고의 이름을 수정합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["put"],
#         name="update_refrigerator",
#         url_path="update/<int:pk>",
#     )
#     def update_refrigerator(self, request, pk=None):
#         """
#         기존 냉장고 이름 수정
#         """
#         return Response({"message": "기존 냉장고 이름 수정 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Refrigerator"],
#         operation_summary="기존 냉장고 삭제",
#         operation_description="기존 냉장고를 삭제합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["delete"],
#         name="delete_refrigerator",
#         url_path="delete/<int:pk>",
#     )
#     def delete_refrigerator(self, request, pk=None):
#         """
#         기존 냉장고 삭제
#         """
#         return Response({"message": "기존 냉장고 삭제 API (미구현)"})


# class RefrigeratorIngredientViewSet(viewsets.ViewSet):
#     """
#     냉장고 재료 관련 API
#     """

#     @swagger_auto_schema(
#         tags=["Refrigerator Ingredient"],
#         operation_summary="냉장고에 새로운 재료 추가",
#         operation_description="냉장고에 새로운 재료를 추가합니다.",
#         manual_parameters=[
#             openapi.Parameter(
#                 "refrigerator_id",
#                 openapi.IN_PATH,
#                 description="냉장고 ID",
#                 type=openapi.TYPE_INTEGER,
#                 required=True,
#             ),
#         ],
#     )
#     @action(
#         detail=True,
#         methods=["post"],
#         name="add_ingredient",
#         url_path="add_ingredient/<int:refrigerator_id>",
#     )
#     def add_ingredient(self, request, refrigerator_id):
#         """
#         냉장고에 새로운 재료 추가
#         """
#         return Response(
#             {"message": f"냉장고 {refrigerator_id}에 새로운 재료 추가 API (미구현)"}
#         )

#     @swagger_auto_schema(
#         tags=["Refrigerator Ingredient"],
#         operation_summary="냉장고에 재료 삭제",
#         operation_description="냉장고에 있는 재료를 삭제합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["delete"],
#         name="remove_ingredient",
#         url_path="remove_ingredient/<int:pk>",
#     )
#     def remove_ingredient(self, request, pk=None):
#         """
#         냉장고에 재료 삭제
#         """
#         return Response({"message": "냉장고에 재료 삭제 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Refrigerator Ingredient"],
#         operation_summary="냉장고내 모든 재료 조회",
#         operation_description="냉장고에 있는 모든 재료를 조회합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["get"],
#         name="list_ingredients",
#         url_path="list_ingredients/<int:pk>",
#     )
#     def list_ingredients(self, request, pk=None):
#         """
#         냉장고내 모든 재료 조회
#         """
#         return Response({"message": "냉장고내 모든 재료 조회 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Refrigerator Ingredient"],
#         operation_summary="냉장고 재료 수정",
#         operation_description="냉장고에 있는 재료 정보를 수정합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["put"],
#         name="update_ingredient",
#         url_path="update_ingredient/<int:pk>",
#     )
#     def update_ingredient(self, request, pk=None):
#         """
#         냉장고 재료 수정
#         """
#         return Response({"message": "냉장고 재료 수정 API (미구현)"})
