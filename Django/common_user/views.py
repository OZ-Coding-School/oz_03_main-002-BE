from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import EmailVerificationToken
from .utils import send_verification_email

# Create your views here.

User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False  # 이메일 인증 전까지 계정을 비활성화 처리
            user.save()
            refresh = RefreshToken.for_user(user)
            token = EmailVerificationToken.objects.create(user=user) # 이메일 인증 토큰 생성
            send_verification_email(user, token.token) # 인증 이메일 발송
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': '회원가입이 완료되었습니다. 이메일을 확인하여 계정을 활성화해주세요.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username_or_email']
            password = serializer.validated_data['password']

            # 이메일 또는 아이디로 로그인 시도
            user = None
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    pass

            if not user:
                user = authenticate(username=username_or_email, password=password)
            else:
                if not user.check_password(password):
                    user = None

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class VerifyEmailView(APIView):
        def get(self, request, token):
            try:
                verification_token = EmailVerificationToken.objects.get(token=token)
                if verification_token.is_valid():
                    user = verification_token.user
                    user.is_active = True
                    user.save()
                    verification_token.delete()
                    return Response({'message': '이메일이 성공적으로 인증되었습니다.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            except EmailVerificationToken.DoesNotExist:
                return Response({'error': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)