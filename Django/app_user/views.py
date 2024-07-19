# app_user/views.py
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter


class UserLoginViewSet(viewsets.GenericViewSet):
    """
    사용자 로그인 관련 API
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
