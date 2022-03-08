from django.db import models
from django.contrib.auth.models import AbstractUser

# custom user class that extends the default user class
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']  

