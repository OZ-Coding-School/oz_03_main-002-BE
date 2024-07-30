from django import forms

from .models import App_User


class CompleteSocialSignupForm(forms.ModelForm):
    nick_name = forms.CharField(max_length=255, label="닉네임")

    class Meta:
        model = App_User
        fields = ["username"]  # 'email' 필드 제외
