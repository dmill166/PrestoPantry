from django.db import models
from prestopantry_app.models.users import User


class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient_id = models.IntegerField()
    ingredient_name = models.CharField(max_length=300)
    upc = models.BigIntegerField()