from django.contrib import admin

from .models import Refrigerator
from .models import RefrigeratorIngredientList


class RefrigeratorIngredientListInline(admin.TabularInline):
    model = RefrigeratorIngredientList
    extra = 1


class RefrigeratorAdmin(admin.ModelAdmin):
    inlines = [RefrigeratorIngredientListInline]
    list_display = ("user", "created_at", "updated_at", "is_activate")
    list_filter = ("user", "is_activate")


admin.site.register(Refrigerator, RefrigeratorAdmin)
