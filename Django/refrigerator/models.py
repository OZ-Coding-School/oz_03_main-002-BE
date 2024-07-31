from django.db import models
from django.conf import settings
from ingredient.models import Ingredient

class Refrigerator(models.Model):
    """
    냉장고 모델: 사용자의 냉장고 정보를 저장합니다.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refrigerators')
    name = models.CharField(max_length=100)  # 냉장고 이름
    brand = models.CharField(max_length=100, blank=True, null=True)  # 브랜드 (선택사항)
    purchase_year = models.IntegerField(blank=True, null=True)  # 구입연도 (선택사항)
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일
    is_active = models.BooleanField(default=True)  # 활성화 여부

    def __str__(self):
        return f"{self.user.username}'s {self.name}"

class RefrigeratorIngredient(models.Model):
    """
    냉장고 내 식재료 모델: 각 냉장고에 있는 식재료의 정보를 저장합니다.
    """
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    expiration_date = models.DateField()  # 유통기한
    quantity = models.FloatField(default=1)  # 수량
    unit = models.CharField(max_length=20, default='개')  # 단위 (예: 개, g, ml 등)

    def __str__(self):
        return f"{self.ingredient.name} in {self.refrigerator.name}"