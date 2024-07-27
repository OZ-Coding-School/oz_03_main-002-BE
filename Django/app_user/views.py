from django.views import View
from django.http import JsonResponse
from rest_framework import status
from .models import App_User
from allauth.socialaccount.models import SocialAccount, SocialLogin
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CompleteSocialSignupForm
import logging
import os
import requests
from json import JSONDecodeError
from django.urls import reverse
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.account.views import SignupView
from allauth.account.utils import complete_signup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 환경 변수 로드 (예: .env 파일 사용 시)
# from dotenv import load_dotenv
# load_dotenv()

state = os.environ.get("STATE")
BASE_URL = 'http://127.0.0.1:8000/'  # 로컬 개발 환경 기준
GOOGLE_CALLBACK_URI = BASE_URL + 'api/v1/google/callback/'


# 구글 로그인 URL 생성
def google_login(request):
    """
    구글 OAuth2 로그인 URL을 생성하여 리디렉션합니다.
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"  # 요청할 사용자 정보 범위
    client_id = os.environ.get("GOOGLE_CLIENT_ID")  # 구글 클라이언트 ID
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )
    
# 구글 로그인 콜백 처리
class GoogleLoginCallbackView(View):
    def get(self, request):
        """
        구글 로그인 콜백을 처리합니다.
        1. authorization code를 사용하여 access token을 얻습니다.
        2. access token을 사용하여 사용자 정보(email)를 얻습니다.
        3. 기존 사용자인지 확인하고, 신규 사용자라면 추가 정보 입력 폼으로 리디렉션합니다.
        """
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        code = request.GET.get('code')

        # 1. 받은 코드로 구글에 access token 요청
        token_req = requests.post(
            f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
        )

        # 1-1. JSO   N 응답 파싱 및 에러 처리
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)

        # 1-2. 성공 시 access_token 가져오기
        access_token = token_req_json.get('access_token')

        # 2. 가져온 access_token으로 사용자 정보를 구글에 요청 (people.get API 사용)
        people_api_response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={'access_token': access_token, 'alt': 'json'}
        )
        people_api_response_json = people_api_response.json()

        # 2-1. 에러 발생 시 400 에러 반환
        if people_api_response.status_code != 200:
            return JsonResponse({'err_msg': 'failed to get user info'}, status=status.HTTP_400_BAD_REQUEST)

        # 2-2. 성공 시 이메일 및 추가 정보 가져오기
        email = people_api_response_json.get('email')
        user_id = people_api_response_json.get('id')  # 구글 사용자 ID
        social_data = people_api_response_json

        logger.debug(f"Social Login Data: {social_data}")

        try:
            # 기존 사용자 확인 (SocialAccount를 통해 User 객체 가져오기)
            social_account = SocialAccount.objects.get(provider=GoogleProvider.id, uid=user_id)
            user = social_account.user

            # 로그인 처리
            login(request, user)

            # access_token을 포함한 JSON 응답 반환
            return JsonResponse({'access_token': access_token})
        except SocialAccount.DoesNotExist:
            # 신규 사용자 처리
            user = App_User.objects.create_user(
                user_id=social_data['email'].split('@')[0],
                email=social_data['email'],
                username=social_data.get('given_name', '') + social_data.get('family_name', ''),
                nick_name=social_data.get('given_name', '') + social_data.get('family_name', ''),
                password=None,
            )

            # SocialAccount 생성 및 저장
            social_account = SocialAccount(
                user=user,
                provider=GoogleProvider.id,
                uid=social_data['id'],
                extra_data=social_data,
            )
            social_account.save()

            # SocialLogin 생성 및 세션에 저장
            sociallogin = SocialLogin(user=user, account=social_account)
            request.session["sociallogin"] = sociallogin.serialize()

            # access_token을 포함한 JSON 응답 반환
            return JsonResponse({'access_token': access_token})


# 소셜 로그인 추가 정보 입력 폼
class CompleteSocialSignupView(SignupView):
    form_class = CompleteSocialSignupForm  # 폼 클래스 지정

    def get(self, request, *args, **kwargs):
        if not request.session.get('sociallogin'):
            return redirect(reverse('user:google_login'))  # 앱 이름을 사용하여 reverse

        # sociallogin 데이터 가져오기
        sociallogin = SocialLogin.deserialize(request.session.get('sociallogin'))

        # 폼 초기화
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # form.fields["email"].initial = sociallogin.user.email

        return self.render_to_response(self.get_context_data(form=form, sociallogin=sociallogin))

    def form_valid(self, form):
        # 폼 유효성 검사 통과 시 회원가입 완료 처리
        sociallogin = SocialLogin.deserialize(self.request.session.get('sociallogin'))
        user = sociallogin.user
        user.user_id = sociallogin.user.email.split('@')[0]
        user.nick_name = form.cleaned_data.get('nick_name') or user.username
        user.username = form.cleaned_data.get('username')
        user.save()
        return complete_signup(self.request, sociallogin, self.get_redirect_url())




# # app_user/views.py
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from allauth.socialaccount.models import SocialAccount

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# import os

# # from dotenv import load_dotenv

# # load_dotenv()
# state = os.environ.get("STATE")
# BASE_URL = 'http://127.0.0.1:8000/'
# GOOGLE_CALLBACK_URI = BASE_URL + 'api/v1/google/callback/'

# from django.shortcuts import redirect
# # 구글 로그인
# def google_login(request):
#     scope = "https://www.googleapis.com/auth/userinfo.email"
#     client_id = os.environ.get("GOOGLE_CLIENT_ID")
#     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

# from json import JSONDecodeError
# from django.http import JsonResponse
# import requests

# from rest_framework import status
# from .models import *
# def get_response():
#     # 기존의 redirect('/accounts/profile/') 대신
#     return redirect(reverse('complete_social_signup'))  # 추가 정보 입력 폼으로 리디렉션


# def google_callback(request):
#     client_id = os.environ.get("GOOGLE_CLIENT_ID")
#     client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
#     code = request.GET.get('code')

#     # 1. 받은 코드로 구글에 access token 요청
#     token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    
#     ### 1-1. json으로 변환 & 에러 부분 파싱
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")

#     ### 1-2. 에러 발생 시 종료
#     if error is not None:
#         raise JSONDecodeError(error)

#     ### 1-3. 성공 시 access_token 가져오기
#     access_token = token_req_json.get('access_token')

#     #################################################################

#     # 2. 가져온 access_token으로 이메일값을 구글에 요청
#     email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
#     email_req_status = email_req.status_code

#     ### 2-1. 에러 발생 시 400 에러 반환
#     if email_req_status != 200:
#         return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
#     ### 2-2. 성공 시 이메일 가져오기
#     email_req_json = email_req.json()
#     email = email_req_json.get('email')

#     # return JsonResponse({'access': access_token, 'email':email})

#     #################################################################

#     # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
#     try:
#         # 전달받은 이메일로 등록된 유저가 있는지 탐색
#         user = App_User.objects.get(email=email)

#         # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
#         social_user = SocialAccount.objects.get(user=user)

#         # 있는데 구글계정이 아니어도 에러
#         if social_user.provider != 'google':
#             return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

#         # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(f"{BASE_URL}api/v1/google/login/finish/", data=data)
#         accept_status = accept.status_code

#         # 뭔가 중간에 문제가 생기면 에러
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)

#     except App_User.DoesNotExist:
#         # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
#         data = {'access_token': access_token, 'code': code}
#         print(data)
#         accept = requests.post(f"{BASE_URL}api/v1/google/login/finish/", data=data)
#         accept_status = accept.status_code

#         # 뭔가 중간에 문제가 생기면 에러
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
        

# # views.py
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from allauth.socialaccount.providers.google import views as google_view

# class GoogleLogin(SocialLoginView):
#     adapter_class = google_view.GoogleOAuth2Adapter
#     callback_url = GOOGLE_CALLBACK_URI
#     client_class = OAuth2Client
    
    
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from allauth.socialaccount.models import SocialLogin
# from .forms import CompleteSocialSignupForm

# def complete_social_signup(request):
#     if not request.session.get('sociallogin'):
#         return redirect('account_login')

#     sociallogin = SocialLogin.deserialize(request.session.get('sociallogin'))

#     if request.method == "POST":
#         form = CompleteSocialSignupForm(request.POST)
#         if form.is_valid():
#             sociallogin.user.user_id = form.cleaned_data['user_id']
#             sociallogin.user.nick_name = form.cleaned_data['nick_name']
#             sociallogin.save(request)
#             del request.session['sociallogin']
#             login(request, sociallogin.user)
#             return redirect('home')  # 홈 페이지로 리다이렉트
#     else:
#         form = CompleteSocialSignupForm()

#     return render(request, 'complete_social_signup.html', {'form': form})



class UserLoginViewSet(viewsets.GenericViewSet):
    """
    사용자 로그인 관련 API
    """

    # 소셜 사용자 로그인
    # @swagger_auto_schema(
    #     tags=["UserLogin"],
    #     operation_summary="소셜 로그인",
    #     operation_description="구글 소셜 로그인을 이용하여 로그인합니다.",
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             "username": openapi.Schema(type=openapi.TYPE_STRING),
    #             "password": openapi.Schema(type=openapi.TYPE_STRING),
    #         },
    #     ),
    #     responses={
    #         201: openapi.Response(
    #             description="로그인 성공 시, 사용자 정보 및 토큰을 반환합니다."
    #         ),
    #         401: openapi.Response(
    #             description="아이디 또는 비밀번호가 일치하지 않을 경우."
    #         ),
    #         400: openapi.Response(description="요청 데이터가 유효하지 않을 경우."),
    #     },
    # )
    # @action(detail=False, methods=["post"], name="google_login", url_path="google/login")
    # def user_social_login_id(self, request):
    #     """
    #     아이디로 사용자 로그인
    #     """
    #     return Response({"message": "아이디 로그인 API (미구현)"})
    

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
