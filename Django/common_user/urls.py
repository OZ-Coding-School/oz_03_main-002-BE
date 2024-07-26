from django.urls import path
from .views import UserRegistrationView, UserLoginView, VerifyEmailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
]