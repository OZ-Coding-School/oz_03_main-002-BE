import os

import requests
from app_user.models import App_User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()
state = os.environ.get("STATE")


# --- Google OAuth 관련 ---
class GoogleLogin(View):
    """
    Google 소셜 로그인을 위한 뷰입니다.

    Google OAuth 2.0 프로토콜을 사용하여 사용자를 인증하고,
    로그인 URL을 생성하여 Google 로그인 페이지로 리디렉션합니다.
    """

    def get(self, request):
        """
        Google 소셜 로그인 URL을 생성합니다.

        **요청:**
        - GET 요청

        **응답:**
        - 302 Redirect: Google 로그인 페이지로 리디렉션
        """
        scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
        redirect_uri = settings.GOOGLE_CALLBACK_URI
        return redirect(
            f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&state={state}"
        )


class GoogleCallback(View):
    """
    Google OAuth 콜백을 처리하는 뷰입니다.

    Google 인증 서버로부터 받은 Authorization Code를 사용하여 액세스 토큰을 획득하고,
    사용자 정보를 가져와 Django 애플리케이션에 로그인 처리를 수행합니다.
    """

    def get(self, request):
        """
        Google OAuth 콜백을 처리합니다.

        **요청:**
        - GET 요청

        **쿼리 매개변수:**
        - code: Google 인증 서버에서 발급한 Authorization Code

        **응답:**
        - 200 OK: 로그인 성공 및 JWT 토큰 반환
        - 400 Bad Request: 액세스 토큰 획득 실패, 사용자 정보 획득 실패, 기타 오류 발생
        """
        with transaction.atomic():
            try:
                code = request.GET.get("code")
                if not code:
                    return JsonResponse({"error": "Invalid code"}, status=400)

                # 액세스 토큰 얻기
                token_response = requests.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "redirect_uri": settings.GOOGLE_CALLBACK_URI,
                        "grant_type": "authorization_code",
                    },
                )

                if token_response.status_code != 200:
                    return JsonResponse(
                        {"error": "Failed to get access token"}, status=400
                    )

                access_token = token_response.json()["access_token"]

                # 사용자 정보 얻기
                user_info_response = requests.get(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    params={"access_token": access_token},
                )

                if user_info_response.status_code != 200:
                    return JsonResponse(
                        {"error": "Failed to get user info"}, status=400
                    )

                user_info = user_info_response.json()
                email = user_info["email"]

                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        email=email,
                        username=user_info.get("name", ""),
                        nick_name=user_info.get("name", ""),
                        user_id=email.split("@")[0],
                    )

                login(request, user)

                # JWT 토큰 발급
                pair_view = CustomTokenObtainPairView()
                factory = APIRequestFactory()
                drf_request = factory.post(
                    "/token/", {"email": user.email, "password": "dummy_password"}
                )
                drf_request.user = authenticate(
                    request, username=user.email, password="dummy_password"
                )
                pair_view.request = drf_request
                pair_view.user = user
                response = pair_view.post(drf_request)

                content = JSONRenderer().render(response.data)
                return HttpResponse(
                    content,
                    content_type="application/json",
                    status=response.status_code,
                )

            except Exception as e:
                print(f"Error in Google callback: {str(e)}")
                error_data = {"status": "error", "message": str(e)}
                return JsonResponse(error_data, status=400)


# --- JWT 관련 ---


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    사용자 지정 JWT 토큰 쌍을 발급하는 뷰입니다.

    이메일과 비밀번호를 사용하여 사용자를 인증하고,
    액세스 토큰과 리프레시 토큰을 발급합니다.
    """

    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["Google-Login"],
        operation_summary="JWT 토큰 획득",
        operation_description="이메일과 비밀번호를 사용하여 JWT 토큰 쌍(액세스 토큰, 리프레시 토큰)을 발급합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="로그인 성공 시, 액세스 토큰과 리프레시 토큰을 반환합니다."
            ),
            401: openapi.Response(
                description="이메일 또는 비밀번호가 일치하지 않을 경우."
            ),
            400: openapi.Response(description="요청 데이터가 유효하지 않을 경우."),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        JWT 토큰 쌍을 발급합니다.

        **요청:**
        - POST 요청

        **요청 본문:**
        - email: 사용자 이메일
        - password: 사용자 비밀번호

        **응답:**
        - 200 OK: 로그인 성공 시, 액세스 토큰과 리프레시 토큰을 반환합니다.
        - 401 Unauthorized: 이메일 또는 비밀번호가 일치하지 않을 경우.
        - 400 Bad Request: 요청 데이터가 유효하지 않을 경우.
        """
        if hasattr(self, "user"):
            user = self.user
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({"access": access_token, "refresh": str(refresh)})
        user.refresh_token = str(refresh)
        user.save()

        return response


class BlacklistTokenUpdateView(TokenBlacklistView):
    """
    Refresh 토큰을 블랙리스트에 추가하고 사용자 모델에서 삭제하는 뷰입니다.

    주로 로그아웃 기능을 구현할 때 사용됩니다.
    """

    @swagger_auto_schema(
        tags=["Google-Login"],
        operation_summary="JWT 토큰 블랙리스트 추가",
        operation_description="로그아웃 시, Refresh 토큰을 블랙리스트에 추가하고 사용자 모델에서 삭제합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh 토큰"
                ),
            },
        ),
        responses={
            205: openapi.Response(description="로그아웃 성공"),
            400: openapi.Response(
                description="Refresh 토큰이 유효하지 않거나, 요청 데이터에 Refresh 토큰이 없는 경우"
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Refresh 토큰을 블랙리스트에 추가하고 사용자 모델에서 삭제합니다.

        **요청:**
        - POST 요청

        **요청 본문:**
        - refresh: 블랙리스트에 추가할 Refresh 토큰

        **응답:**
        - 205 Reset Content: 로그아웃 성공
        - 400 Bad Request: Refresh 토큰이 유효하지 않거나, 요청 데이터에 Refresh 토큰이 없는 경우
        """
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                user_id = token.payload.get(api_settings.USER_ID_CLAIM)
                if user_id:
                    user = App_User.objects.get(id=user_id)
                    user.refresh_token = None
                    user.save()

                response = Response(status=status.HTTP_205_RESET_CONTENT)
                response.delete_cookie("refresh")
                return response

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Refresh token not found in cookie"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh 토큰을 사용하여 액세스 토큰을 갱신하는 뷰입니다.

    Refresh 토큰이 유효하면 새로운 액세스 토큰을 발급하고,
    토큰 순환 설정이 활성화된 경우에는 기존 Refresh 토큰을 블랙리스트에 추가합니다.
    """

    @swagger_auto_schema(
        tags=["Google-Login"],
        operation_summary="JWT 토큰 갱신",
        operation_description="Refresh 토큰을 사용하여 액세스 토큰을 갱신합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Refresh 토큰"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="액세스 토큰 갱신 성공, 새로운 액세스 토큰과 리프레시 토큰 반환"
            ),
            401: openapi.Response(description="Refresh 토큰이 유효하지 않은 경우"),
            400: openapi.Response(description="요청 데이터에 Refresh 토큰이 없는 경우"),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Refresh 토큰을 사용하여 액세스 토큰을 갱신합니다.

        **요청:**
        - POST 요청

        **요청 본문:**
        - refresh: 액세스 토큰 갱신에 사용할 Refresh 토큰

        **응답:**
        - 200 OK: 액세스 토큰 갱신 성공, 새로운 액세스 토큰과 리프레시 토큰 반환
        - 401 Unauthorized: Refresh 토큰이 유효하지 않은 경우
        - 400 Bad Request: 요청 데이터에 Refresh 토큰이 없는 경우
        """
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token not found in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            serializer = self.get_serializer(data={"refresh": str(token)})
            serializer.is_valid(raise_exception=True)
            response_data = serializer.validated_data

            if api_settings.ROTATE_REFRESH_TOKENS:
                try:
                    token.blacklist()
                except TokenError:
                    pass

            user_id = token.payload[api_settings.USER_ID_CLAIM]
            user = App_User.objects.get(id=user_id)
            refresh = RefreshToken.for_user(user)
            response_data["refresh"] = str(refresh)

            user = App_User.objects.get(id=token.payload[api_settings.USER_ID_CLAIM])
            user.refresh_token = str(refresh)
            user.save()

            return Response(response_data)

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


# --- DRF Yasg ---
class UserLoginViewSet(viewsets.GenericViewSet):
    """
    사용자 로그인 관련 API (미구현)
    """

    # 아이디로 사용자 로그인
    @swagger_auto_schema(
        tags=["UserLogin"],
        operation_summary="아이디 로그인",
        operation_description="아이디와 비밀번호를 사용하여 로그인합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response(
                description="로그인 성공 시, 사용자 정보 및 토큰을 반환합니다."
            ),
            401: openapi.Response(
                description="아이디 또는 비밀번호가 일치하지 않을 경우."
            ),
            400: openapi.Response(description="요청 데이터가 유효하지 않을 경우."),
        },
    )
    @action(detail=False, methods=["post"], name="id_login", url_path="id")
    def user_login_id(self, request):
        """
        아이디로 사용자 로그인
        """
        return Response({"message": "아이디 로그인 API (미구현)"})

    # 이메일로 사용자 로그인
    @swagger_auto_schema(
        tags=["UserLogin"],
        operation_summary="이메일 로그인",
        operation_description="이메일과 비밀번호를 사용하여 로그인합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response(
                description="로그인 성공 시, 사용자 정보 및 토큰을 반환합니다."
            ),
            401: openapi.Response(
                description="이메일 또는 비밀번호가 일치하지 않을 경우."
            ),
            400: openapi.Response(description="요청 데이터가 유효하지 않을 경우."),
        },
    )
    @action(detail=False, methods=["post"], name="email_login", url_path="email")
    def user_login_email(self, request):
        """
        이메일로 사용자 로그인
        """
        return Response({"message": "이메일 로그인 API (미구현)"})


class UserSignInViewSet(viewsets.GenericViewSet):
    """
    사용자 회원가입 관련 API
    """

    # 소셜 회원 가입
    @swagger_auto_schema(
        tags=["Sign-In"],
        operation_summary="구글 소셜 회원 가입",
        operation_description="사용자가 구글 API를 이용해 회원가입을 합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 아이디"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
            required=["username", "password"],  # 필수 필드 추가
        ),
        responses={
            201: openapi.Response(
                description="회원가입 성공. 사용자 정보 및 토큰 반환",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="요청 데이터가 유효하지 않을 경우 (예: 중복된 아이디)"
            ),
        },
    )
    @action(detail=False, methods=["post"], name="google", url_path="google/signin")
    def user_social_sign_in(self, request):
        """
        사용자 회원 가입
        """
        return Response({"message": "사용자 회원 가입 API (미구현)"})

    @swagger_auto_schema(
        tags=["Sign-In"],
        operation_summary="회원 가입",
        operation_description="사용자가 회원가입을 합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 아이디"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
            required=["username", "password"],  # 필수 필드 추가
        ),
        responses={
            201: openapi.Response(
                description="회원가입 성공. 사용자 정보 및 토큰 반환",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "token": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="요청 데이터가 유효하지 않을 경우 (예: 중복된 아이디)"
            ),
        },
    )
    @action(detail=False, methods=["post"], name="signin", url_path="signin")
    def user_sign_in(self, request):
        """
        사용자 회원 가입
        """
        return Response({"message": "사용자 회원 가입 API (미구현)"})


class UserAccountRecoveryViewSet(viewsets.GenericViewSet):
    """
    사용자 계정 복구 관련 API
    """

    @swagger_auto_schema(
        tags=["Account Recovery"],
        operation_summary="비밀번호 찾기",
        operation_description="이메일을 통해 비밀번호 재설정 링크를 전송합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 이메일"
                )
            },
        ),
        responses={
            200: openapi.Response(description="비밀번호 재설정 링크 전송 성공"),
            404: openapi.Response(
                description="해당 이메일로 가입된 사용자를 찾을 수 없음"
            ),
            400: openapi.Response(description="요청 데이터가 유효하지 않을 경우"),
        },
    )
    @action(
        detail=False, methods=["post"], name="find_password", url_path="find_password"
    )
    def find_password(self, request):
        """
        비밀번호 찾기
        """
        return Response({"message": "비밀번호 찾기 API (미구현)"})

    @swagger_auto_schema(
        tags=["Account Recovery"],
        operation_summary="아이디 찾기",
        operation_description="이름과 전화번호를 통해 아이디를 찾습니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 이름"
                ),
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="전화번호"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="아이디 찾기 성공"),
            404: openapi.Response(
                description="해당 정보로 가입된 사용자를 찾을 수 없음"
            ),
            400: openapi.Response(description="요청 데이터가 유효하지 않을 경우"),
        },
    )
    @action(detail=False, methods=["post"], name="find_id", url_path="find_id")
    def find_id(self, request):
        """
        아이디 찾기
        """
        return Response({"message": "아이디 찾기 API (미구현)"})

    @swagger_auto_schema(
        tags=["Account Recovery"],
        operation_summary="비밀번호 재설정",
        operation_description="새로운 비밀번호로 재설정합니다. (비밀번호 찾기를 통해 전달받은 토큰 필요)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "token": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호 재설정 토큰"
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="새로운 비밀번호"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="비밀번호 재설정 성공"),
            400: openapi.Response(
                description="요청 데이터가 유효하지 않거나 토큰이 유효하지 않을 경우"
            ),
        },
    )
    @action(
        detail=False, methods=["post"], name="reset_password", url_path="reset_password"
    )
    def reset_password(self, request):
        """
        비밀번호 재설정
        """
        return Response({"message": "비밀번호 재설정 API (미구현)"})


class UserRefrigeratorViewSet(viewsets.ViewSet):  # ListModelMixin 제거
    """
    유저 냉장고 목록 관련 API
    """

    @swagger_auto_schema(
        tags=["Refrigerator-List"],
        operation_summary="유저 냉장고 목록 불러오기",
        operation_description="로그인한 유저의 냉장고 목록을 불러옵니다.",
        responses={
            200: openapi.Response(
                description="냉장고 목록 조회 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, description="냉장고 ID"
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING, description="냉장고 이름"
                            ),
                            # ... 필요한 냉장고 정보 필드 추가 ...
                        },
                    ),
                ),
            ),
            401: openapi.Response(description="로그인이 필요합니다."),
        },
    )
    @action(detail=False, methods=["get"], name="list_refrigerators", url_path="list")
    def list_refrigerators(self, request):
        """
        유저 냉장고 목록 불러오기
        """
        return Response({"message": "유저 냉장고 목록 불러오기 API (미구현)"})
