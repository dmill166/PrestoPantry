from django.db import models
# from django.contrib.auth.models import User


class User(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=64)
    begin_date = models.DateField()
    end_date = models.DateField()
    current_ind = models.BooleanField()
    created_record = models.DateTimeField()
    modified_record = models.DateTimeField()
