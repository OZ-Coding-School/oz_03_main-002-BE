from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.username = f"{user.last_name}{user.first_name}"
        if commit:
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        
        if not user.user_id or not user.nick_name:
            # Store the sociallogin object in the session
            request.session['sociallogin'] = sociallogin.serialize()
            return redirect(reverse('complete_social_signup'))

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.username = sociallogin.account.extra_data.get('name', '') 
        user.save()
        return user