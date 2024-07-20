from django.db import models


class IngreMajor(models.Model):
    name = models.CharField(max_length=255)


class IngreMiddle(models.Model):
    name = models.CharField(max_length=255)
    major = models.ForeignKey(IngreMajor, on_delete=models.CASCADE)


class IngreSub(models.Model):
    name = models.CharField(max_length=255)
    middle = models.ForeignKey(IngreMiddle, on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    major = models.ForeignKey(IngreMajor, on_delete=models.CASCADE)
    middle = models.ForeignKey(IngreMiddle, on_delete=models.CASCADE)
    sub = models.ForeignKey(IngreSub, on_delete=models.CASCADE)
