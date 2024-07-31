import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except InvalidToken as e:
            logger.error(f"Invalid token: {str(e)}")
            raise
        except TokenError as e:
            logger.error(f"Token error: {str(e)}")
            raise