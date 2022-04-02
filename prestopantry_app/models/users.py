from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# custom user class that extends the default user class
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z]+$', message='First name must be letters only.')])
    last_name = models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z]+$', message='Last name must be letters only.')])
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def oauth_user(self):
        return not self.has_usable_password()
