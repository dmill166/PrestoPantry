from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from prestopantry_app.models.developers import Developer
from prestopantry_app.models.users import User
from prestopantry_app.models.user_ingredients import UserIngredient


class UserIngredientInline(admin.TabularInline):
    model = UserIngredient
    extra = 0
    readonly_fields = ('ingredient_name', 'ingredient_id', 'upc')
  

class UserAdmin(UserAdmin):
    inlines = (UserIngredientInline,)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Developer)
admin.site.register(UserIngredient)
