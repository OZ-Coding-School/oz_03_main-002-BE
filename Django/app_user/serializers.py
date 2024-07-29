from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomTokenObtainPairSerializer(TokenRefreshSerializer):
    """
    JWT 토큰 갱신을 위한 커스텀 시리얼라이저
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = str(user.id)
        return token
