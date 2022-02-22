from django.db import models
from prestopantry_app.models.users import User


class UserIngredients(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient_id = models.IntegerField()
    begin_date = models.DateField()
    end_date = models.DateField()
    current_ind = models.BooleanField()
    created_record = models.DateTimeField()
    modified_record = models.DateTimeField()
