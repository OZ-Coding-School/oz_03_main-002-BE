from django.contrib import admin

from .models import Ingredient, IngreMajor, IngreMiddle, IngreSub

admin.site.register(Ingredient)
admin.site.register(IngreMajor)
admin.site.register(IngreMiddle)
admin.site.register(IngreSub)
