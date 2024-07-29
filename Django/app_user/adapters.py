"""
Google OAuth2 관련 커스텀 어댑터 및 유틸리티 함수
"""
from django.conf import settings
from django.http import JsonResponse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from .models import App_User  # User 모델 경로 확인

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    """
    Google OAuth2 인증을 위한 커스텀 어댑터
    """
    def complete_login(self, request, app, token, **kwargs):
        """
        Google 로그인 완료 후 사용자 정보를 가져와 SocialLogin 객체를 반환합니다.
        """
        provider = self.get_provider()
        app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        extra_data = kwargs["response"].json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

    def get_app(self, request, provider):
        """
        주어진 요청과 provider에 대한 SocialApp을 반환합니다.
        여러 개의 SocialApp이 존재할 경우 첫 번째 항목을 반환하고,
        존재하지 않을 경우 None을 반환합니다.
        """
        try:
            return SocialApp.objects.get(provider=provider.id, sites__id=settings.SITE_ID)
        # except SocialApp.MultipleObjectsReturned:
        #     return SocialApp.objects.filter(provider=provider.id, sites__id=settings.SITE_ID).first()
        except SocialApp.DoesNotExist:
            return None

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    소셜 계정 어댑터: 소셜 로그인 전후 처리를 커스터마이징합니다.
    """
    def pre_social_login(self, request, sociallogin):
        """
        소셜 로그인 전에 기존 사용자인지 확인하고 연결합니다.
        """
        user = sociallogin.user
        if user.id:  # 이미 연결된 사용자면 종료
            return

        try:
            existing_user = App_User.objects.get(email=user.email)
            sociallogin.connect(request, existing_user)  # 기존 사용자와 연결
        except App_User.DoesNotExist:
            pass  # 신규 사용자는 아무 동작 없음

    def respond_user_inactive(self, request, user):
        """
        비활성 사용자에 대한 응답을 JSON 형식으로 반환합니다.
        """
        return JsonResponse({'error': 'User inactive'}, status=400)

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        인증 오류 발생 시 JSON 형식으로 오류 메시지를 반환합니다.
        """
        return JsonResponse({'error': 'Authentication failed'}, status=400)
