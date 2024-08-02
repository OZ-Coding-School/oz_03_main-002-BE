from common.decorators import custom_superuser_required
from common.decorators import login_required_ajax
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe
from .models import RecipeIngredientList
from .models import CookingNameList, CookingMethod, CookingSituation, CookingMainIngre, CookingType
from .serializers import CookingNameListSerializer, CookingMethodSerializer, CookingSituationSerializer, CookingMainIngreSerializer, CookingTypeSerializer
from .serializers import DetailRecipeSerializer
from .serializers import RecipeSerializer


class RecipeListView(APIView):
    """
    레시피 목록 조회 API 뷰 (무한 스크롤)
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 목록 조회 (무한 스크롤)",
        operation_description="무한 스크롤 방식으로 레시피 목록을 조회합니다. last_recipe_id 파라미터를 사용하여 다음 레시피를 가져옵니다.",
        manual_parameters=[
            openapi.Parameter(
                "last_recipe_id",
                openapi.IN_QUERY,
                description="마지막으로 불러온 레시피의 ID",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="레시피 목록 조회 성공",
                schema=RecipeSerializer(many=True),
            ),
        },
    )
    def get(self, request):
        last_recipe_id = request.query_params.get("last_recipe_id")
        page_size = 40

        queryset = Recipe.objects.all().order_by("-created_at")

        if last_recipe_id:
            queryset = queryset.filter(id__lt=last_recipe_id)  # 마지막 레시피 ID보다 작은 레시피만 필터링

        recipes = queryset[:page_size]
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


class RecipeCreateView(APIView):
    """
    레시피 생성 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 생성",
        operation_description="새로운 레시피를 생성합니다.",
        request_body=RecipeSerializer,
        responses={
            201: openapi.Response(
                description="레시피 생성 성공",
                schema=RecipeSerializer,
            ),
            400: openapi.Response(description="잘못된 요청"),
        },
    )
    @login_required_ajax
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            recipe = serializer.save(nick_name=request.user)
            return Response(RecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RecipeDetailView(APIView):
    """
    레시피 상세 조회, 수정, 삭제 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 상세 조회",
        operation_description="레시피 ID로 상세 정보를 조회합니다.",
        responses={
            200: openapi.Response(
                description="레시피 상세 조회 성공",
                schema=RecipeSerializer,
            ),
            404: openapi.Response(description="레시피를 찾을 수 없음"),
        },
    )
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 수정",
        operation_description="레시피 ID로 레시피 정보를 수정합니다. (작성자 또는 관리자만 가능)",
        request_body=RecipeSerializer,
        responses={
            200: openapi.Response(
                description="레시피 수정 성공",
                schema=RecipeSerializer,
            ),
            400: openapi.Response(description="잘못된 요청"),
            403: openapi.Response(description="권한 없음"),
            404: openapi.Response(description="레시피를 찾을 수 없음"),
        },
    )
    @login_required_ajax
    def put(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.user == recipe.nick_name or request.user.is_superuser:
            serializer = RecipeSerializer(recipe, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 삭제",
        operation_description="레시피 ID로 레시피를 삭제합니다. (작성자 또는 관리자만 가능)",
        responses={
            204: openapi.Response(description="레시피 삭제 성공"),
            403: openapi.Response(description="권한 없음"),
            404: openapi.Response(description="레시피를 찾을 수 없음"),
        },
    )
    @login_required_ajax
    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.user == recipe.nick_name or request.user.is_superuser:
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class RecipeFilterView(APIView):
    """
    레시피 필터링 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 필터링",
        operation_description="식재료 이름으로 레시피를 필터링합니다.",
        manual_parameters=[
            openapi.Parameter(
                "ingredients",
                openapi.IN_QUERY,
                description="필터링할 식재료 이름 (여러 개일 경우 쉼표로 구분)",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="필터링된 레시피 목록 조회 성공",
                schema=RecipeSerializer(many=True),
            ),
        },
    )
    def get(self, request):
        ingredients_str = self.request.query_params.get("ingredients", "")
        ingredients = [ing.strip() for ing in ingredients_str.split(",") if ing.strip()]

        queryset = Recipe.objects.all()
        for ingredient_name in ingredients:
            queryset = queryset.filter(
                recipeingredientlist_set__ingredient__name__icontains=ingredient_name
            )

        last_recipe_id = request.query_params.get("last_recipe_id")
        page_size = 40

        if last_recipe_id:
            queryset = queryset.filter(id__lt=last_recipe_id)

        recipes = queryset.distinct()[:page_size]
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)


class DetailRecipeListView(APIView):
    """
    레시피 상세 정보 목록 조회 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="레시피 상세 정보 목록 조회",
        operation_description="레시피 ID로 상세 정보 목록을 조회합니다.",
        responses={
            200: openapi.Response(
                description="레시피 상세 정보 목록 조회 성공",
                schema=DetailRecipeSerializer(many=True),
            ),
            404: openapi.Response(description="레시피를 찾을 수 없음"),
        },
    )
    def get(self, request, recipe_id):
        detail_recipes = DetailRecipe.objects.filter(recipe_id=recipe_id)
        serializer = DetailRecipeSerializer(detail_recipes, many=True)
        return Response(serializer.data)
    
class CookingNameListListView(APIView):
    """
    CookingNameList 목록 조회 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],  # 태그 이름 설정
        operation_summary="CookingNameList 목록 조회",
        operation_description="모든 CookingNameList 객체 목록을 조회합니다.",
        responses={
            200: openapi.Response(
                description="CookingNameList 목록 조회 성공",
                schema=CookingNameListSerializer(many=True),
            )
        }
    )
    def get(self, request):
        queryset = CookingNameList.objects.all()
        serializer = CookingNameListSerializer(queryset, many=True)
        return Response(serializer.data)


class CookingMethodListView(APIView):
    """
    CookingMethod 목록 조회 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="CookingMethod 목록 조회",
        operation_description="모든 CookingMethod 객체 목록을 조회합니다.",
        responses={
            200: openapi.Response(
                description="CookingMethod 목록 조회 성공",
                schema=CookingMethodSerializer(many=True),
            )
        }
    )
    def get(self, request):
        queryset = CookingMethod.objects.all()
        serializer = CookingMethodSerializer(queryset, many=True)
        return Response(serializer.data)


class CookingSituationListView(APIView):
    """
    CookingSituation 목록 조회 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="CookingSituation 목록 조회",
        operation_description="모든 CookingSituation 객체 목록을 조회합니다.",
        responses={
            200: openapi.Response(
                description="CookingSituation 목록 조회 성공",
                schema=CookingSituationSerializer(many=True),
            )
        }
    )
    def get(self, request):
        queryset = CookingSituation.objects.all()
        serializer = CookingSituationSerializer(queryset, many=True)
        return Response(serializer.data)


class CookingMainIngreListView(APIView):
    """
    CookingMainIngre 목록 조회 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="CookingMainIngre 목록 조회",
        operation_description="모든 CookingMainIngre 객체 목록을 조회합니다.",
        responses={
            200: openapi.Response(
                description="CookingMainIngre 목록 조회 성공",
                schema=CookingMainIngreSerializer(many=True),
            )
        }
    )
    def get(self, request):
        queryset = CookingMainIngre.objects.all()
        serializer = CookingMainIngreSerializer(queryset, many=True)
        return Response(serializer.data)


class CookingTypeListView(APIView):
    """
    CookingType 목록 조회 API 뷰
    """

    @swagger_auto_schema(
        tags=["Recipe"],
        operation_summary="CookingType 목록 조회",
        operation_description="모든 CookingType 객체 목록을 조회합니다.",
        responses={
            200: openapi.Response(
                description="CookingType 목록 조회 성공",
                schema=CookingTypeSerializer(many=True),
            )
        }
    )
    def get(self, request):
        queryset = CookingType.objects.all()
        serializer = CookingTypeSerializer(queryset, many=True)
        return Response(serializer.data)