from django.contrib import admin

from .models import Ingredient
from .models import IngreMajor
from .models import IngreMiddle
from .models import IngreSub

admin.site.register(Ingredient)
admin.site.register(IngreMajor)
admin.site.register(IngreMiddle)
admin.site.register(IngreSub)
