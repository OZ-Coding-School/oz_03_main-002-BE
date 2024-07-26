from django.core.mail import send_mail
from django.conf import settings

# 이메일 전송 함수
def send_verification_email(user, token):
    subject = '이메일 주소 확인'
    message = f'다음 링크를 클릭하여 이메일 주소를 확인해주세요: http://yourdomain.com/verify-email/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    send_mail(subject, message, email_from, recipient_list)