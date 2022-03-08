from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class UserAuthBackend(ModelBackend):
    def authenticate(request=None, email=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    
    def email_taken(email):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return False
        else:
            return True

    def username_taken(username):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return False
        else:
            return True
