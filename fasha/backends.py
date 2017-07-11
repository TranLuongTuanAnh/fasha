from django.contrib.auth.models import User
from rest_framework import authentication
from django.contrib.auth.hashers import check_password


from re import sub
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from pprint import pprint

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

class AuthenticationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', header_token)
                token_obj = Token.objects.get(key = token)
                request.user = token_obj.user
            except Token.DoesNotExist:
                request.user = AnonymousUser()
                pass
        else:
            pass
