# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import mixins
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.routers import DefaultRouter

# # 레시피 리스트 조회(GET) : 20개씩 레시피 리스트를 받아오며 상세 정보 없이 받아온다
# # 상세 레시피 조회(GET)
# # 레시피 등록(POST)
# # 레시피 삭제(DELETE)
# # 레시피 수정(PUT)
# # 추천 레시피 리스트 조회(GET) : 20개씩 레시피 리스트를 받아오며 상세 정보 없이 받아온다


# class RecipeListViewSet(viewsets.ViewSet):
#     """
#     레시피 리스트 관련 API
#     """

#     @swagger_auto_schema(
#         tags=["Recipe List"],
#         operation_summary="레시피 리스트 조회",
#         operation_description="20개씩 레시피 리스트를 받아오며 상세 정보 없이 받아옵니다.",
#     )
#     @action(detail=False, methods=["get"], name="list_recipes", url_path="list")
#     def list_recipes(self, request):
#         """
#         레시피 리스트 조회
#         """
#         return Response({"message": "레시피 리스트 조회 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Recipe List"],
#         operation_summary="추천 레시피 리스트 조회",
#         operation_description="20개씩 추천 레시피 리스트를 받아오며 상세 정보 없이 받아옵니다.",
#     )
#     @action(
#         detail=False, methods=["get"], name="recommend_recipes", url_path="recommend"
#     )
#     def recommend_recipes(self, request):
#         """
#         추천 레시피 리스트 조회
#         """
#         return Response({"message": "추천 레시피 리스트 조회 API (미구현)"})


# class RecipeDetailViewSet(viewsets.ViewSet):
#     """
#     상세 레시피 관련 API
#     """

#     @swagger_auto_schema(
#         tags=["Recipe Detail"],
#         operation_summary="상세 레시피 조회",
#         operation_description="레시피의 상세 정보를 조회합니다.",
#     )
#     @action(
#         detail=True, methods=["get"], name="detail_recipe", url_path="detail/<int:pk>"
#     )
#     def retrieve_recipe(self, request, pk=None):
#         """
#         상세 레시피 조회
#         """
#         return Response({"message": "상세 레시피 조회 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Recipe Detail"],
#         operation_summary="레시피 등록",
#         operation_description="새로운 레시피를 등록합니다.",
#     )
#     @action(detail=False, methods=["post"], name="create_recipe", url_path="create")
#     def create_recipe(self, request):
#         """
#         레시피 등록
#         """
#         return Response({"message": "레시피 등록 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Recipe Detail"],
#         operation_summary="레시피 삭제",
#         operation_description="기존 레시피를 삭제합니다.",
#     )
#     @action(
#         detail=True,
#         methods=["delete"],
#         name="delete_recipe",
#         url_path="delete/<int:pk>",
#     )
#     def delete_recipe(self, request, pk=None):
#         """
#         레시피 삭제
#         """
#         return Response({"message": "레시피 삭제 API (미구현)"})

#     @swagger_auto_schema(
#         tags=["Recipe Detail"],
#         operation_summary="레시피 수정",
#         operation_description="기존 레시피를 수정합니다.",
#     )
#     @action(
#         detail=True, methods=["put"], name="update_recipe", url_path="update/<int:pk>"
#     )
#     def update_recipe(self, request, pk=None):
#         """
#         레시피 수정
#         """
#         return Response({"message": "레시피 수정 API (미구현)"})
