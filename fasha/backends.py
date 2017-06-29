from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class AuthByMail(object):
    """docstring for AuthByMail."""

    def authenticate(self,email=None,password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        # Check password of the user we found
        if check_password(password, user.password):
            return user
        return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
