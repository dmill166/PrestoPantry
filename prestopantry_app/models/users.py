from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.timezone import now
from dynamic_preferences.registries import global_preferences_registry


# custom user class that extends the default user class
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z]+$', message='First name must be letters only.')])
    last_name = models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z]+$', message='Last name must be letters only.')])
    last_api_call = models.DateTimeField(default=now)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def oauth_user(self):
        return not self.has_usable_password()

    def allow_api_call(self):
        global_preferences = global_preferences_registry.manager()

        new_api_call = now()
        if (new_api_call - self.last_api_call).total_seconds() > global_preferences['time_between_api_calls']:
            self.last_api_call = new_api_call
            self.save()
            return True
        return False
