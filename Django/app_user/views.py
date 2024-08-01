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
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()
state = os.environ.get("STATE")


# --- Google OAuth 관련 ---
class GoogleLogin(APIView):
    """
    Google 소셜 로그인을 위한 뷰입니다.

    Google OAuth 2.0 프로토콜을 사용하여 사용자를 인증하고,
    로그인 URL을 생성하여 Google 로그인 페이지로 리디렉션합니다.
    """

    @swagger_auto_schema(
        tags=["Google-Login"],
        operation_summary="Google 소셜 로그인 시작",
        operation_description="Google 소셜 로그인 프로세스를 시작합니다. Google 로그인 페이지로 리디렉션됩니다.",
        responses={
            302: openapi.Response(
                description="Google 로그인 페이지로 리디렉션",
                headers={
                    "Location": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Google 인증 URL"
                    )
                },
            )
        },
    )
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


class GoogleCallback(APIView):
    """
    Google OAuth 콜백을 처리하는 뷰입니다.

    Google 인증 서버로부터 받은 Authorization Code를 사용하여 액세스 토큰을 획득하고,
    사용자 정보를 가져와 Django 애플리케이션에 로그인 처리를 수행합니다.
    """

    @swagger_auto_schema(
        tags=["Google-Login"],
        operation_summary="Google 소셜 로그인 콜백",
        operation_description="Google 인증 후 콜백을 처리합니다. 사용자 정보를 받아 로그인 또는 회원가입을 진행합니다.",
        manual_parameters=[
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="Google에서 제공하는 인증 코드",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "state",
                openapi.IN_QUERY,
                description="CSRF 방지를 위한 상태 토큰",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="로그인 성공 및 JWT 토큰 반환",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT 액세스 토큰"
                        ),
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT 리프레시 토큰"
                        ),
                    },
                ),
            ),
            400: openapi.Response(description="잘못된 요청 또는 인증 실패"),
        },
    )
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
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Response 객체 생성 및 쿠키 설정
                response = Response({})
                response.set_cookie(
                    "access", access_token, httponly=True, secure=True, samesite="Lax"
                )
                response.set_cookie(
                    "refresh", str(refresh), httponly=True, secure=True, samesite="Lax"
                )

                # 사용자 모델에 refresh 토큰 저장 (선택 사항)
                user.refresh_token = str(refresh)
                user.save()

                return response

            except requests.exceptions.RequestException as e:
                print(f"Error in Google OAuth request: {str(e)}")
                return JsonResponse(
                    {"error": "Google OAuth request failed"}, status=400
                )

            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

            except Exception as e:
                print(f"Unexpected error in Google callback: {str(e)}")
                return JsonResponse({"error": "Internal server error"}, status=500)


# --- JWT 관련 ---


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    사용자 지정 JWT 토큰 쌍을 발급하는 뷰입니다.

    이메일과 비밀번호를 사용하여 사용자를 인증하고,
    액세스 토큰과 리프레시 토큰을 발급합니다.
    """

    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["JWT"],
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
        # response = Response({"access": access_token, "refresh": str(refresh)})
        # user.refresh_token = str(refresh)
        # user.save()

        # return response
        # 토큰을 쿠키에 저장
        response = Response({"access": access_token, "refresh": str(refresh)})

        # JWT 토큰을 쿠키에 설정
        response.set_cookie(
            "access", access_token, httponly=True, secure=True, samesite="Lax"
        )  # HTTPS만 저장되도록 secure=True)
        response.set_cookie(
            "refresh", str(refresh), httponly=True, secure=True, samesite="Lax"
        )  # HTTPS만 저장되도록 secure=True

        # 사용자 모델에 refresh 토큰 저장 (선택 사항)
        user.refresh_token = str(refresh)
        user.save()

        # return response


class BlacklistTokenUpdateView(TokenBlacklistView):
    """
    Refresh 토큰을 블랙리스트에 추가하고 사용자 모델에서 삭제하는 뷰입니다.

    주로 로그아웃 기능을 구현할 때 사용됩니다.
    """

    @swagger_auto_schema(
        tags=["JWT"],
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
        tags=["JWT"],
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
            # 새로운 리프레시 토큰 생성 및 쿠키 설정
            refresh = RefreshToken.for_user(user)
            response = Response({})
            response.set_cookie(
                "access",
                str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            response.set_cookie(
                "refresh", str(refresh), httponly=True, secure=True, samesite="Lax"
            )

            # 사용자 모델에 새로운 리프레시 토큰 저장
            user.refresh_token = str(refresh)
            user.save()

            return response

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class UserInfoView(APIView):
    """
    액세스 토큰을 사용하여 사용자 정보를 조회하는 API 뷰입니다.
    """
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 설정
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=["User"],
        operation_summary="사용자 정보 조회",
        operation_description="액세스 토큰을 사용하여 사용자 정보(username, user_id, email, is_active)를 조회합니다.",
        responses={
            200: openapi.Response(
                description="사용자 정보 조회 성공",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(type=openapi.TYPE_STRING),
                        "user_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            ),
            401: openapi.Response(description="인증되지 않은 사용자"),
        },
    )
    def get(self, request):
        """
        액세스 토큰으로 사용자 정보를 조회합니다.

        **요청:**
        - GET 요청

        **응답:**
        - 200 OK: 사용자 정보 반환
        - 401 Unauthorized: 인증되지 않은 사용자
        """
        user = request.user  # JWTAuthentication을 통해 인증된 사용자 정보 가져오기

        return Response({
            "username": user.username,
            "user_id": user.user_id,
            "email": user.email,
            "is_active": user.is_active,
        })