from django.contrib import admin

from prestopantry_app.models.developers import Developer
from prestopantry_app.models.users import User
from prestopantry_app.models.user_ingredients import UserIngredient

# Register your models here.
admin.site.register(Developer)
admin.site.register(User)
admin.site.register(UserIngredient)