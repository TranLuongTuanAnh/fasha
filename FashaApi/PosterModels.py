from __future__ import unicode_literals

from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from FashaApi.models import UserSerializer


class Poster(serializers.ModelSerializer):
    owner = serializers.ForeignKey(UserSerializer)
    body = serializers.CharField()
    created = serializers.DateTimeField()
    email = serializers.EmailField()
