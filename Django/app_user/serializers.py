from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import serializers

User = get_user_model()


class GoogleSocialAuthSerializer(serializers.Serializer):
    """
    Google 소셜 로그인 Serializer
    """

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        """
        구글 ID 토큰 검증
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token,
                google_requests.Request(),
                os.environ.get("GOOGLE_CLIENT_ID"),
            )

            if idinfo["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ValueError("Wrong issuer.")

            # 필요한 경우 추가 검증 로직 추가 (예: 이메일 도메인 검증)

            return idinfo
        except ValueError:
            raise serializers.ValidationError("Invalid auth token")

    def get_authorization_url(self):
        """
        구글 OAuth2 인증 URL 생성
        """
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_secrets_file(
            os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRETS_JSON"),
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            redirect_uri=os.environ.get("GOOGLE_CALLBACK_URI"),
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        return authorization_url

    def complete_login(self, request):
        """
        구글 로그인 완료 후 사용자 정보 가져오기 및 로그인 처리
        """
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_secrets_file(
            os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRETS_JSON"),
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            redirect_uri=os.environ.get("GOOGLE_CALLBACK_URI"),
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials

        request_session = google_requests.AuthorizedSession(credentials)
        userinfo_response = request_session.get(
            "https://www.googleapis.com/oauth2/v3/userinfo"
        )
        userinfo_response.raise_for_status()
        data = userinfo_response.json()

        try:
            # 기존 사용자 확인
            social_account = SocialAccount.objects.get(
                provider="google", uid=data["sub"]
            )
            user = social_account.user
            is_new_user = False
        except SocialAccount.DoesNotExist:
            # 신규 사용자 생성
            user = User.objects.create_user(
                email=data["email"],
                username=data.get("name", ""),
            )
            SocialAccount.objects.create(
                provider="google",
                uid=data["sub"],
                user=user,
                extra_data=data,
            )
            is_new_user = True

        return user, is_new_user


class CompleteSocialSignupSerializer(serializers.ModelSerializer):
    """
    소셜 로그인 추가 정보 입력 Serializer
    """

    class Meta:
        model = User
        fields = ["username", "nick_name"]  # 필요한 필드 추가
