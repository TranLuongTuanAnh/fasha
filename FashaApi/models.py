from __future__ import unicode_literals

from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from pprint import pprint
from datetime import datetime

# Create your models here.
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField (
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # username = serializers.CharField
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id','username','email','password')

class Poster(models.Model):
    owner_id = models.EmailField(default='default')
    content = models.CharField(max_length=250)
    created = models.DateTimeField()
    def __init__(self, owner_id, content, created=None):
        super(Poster, self).__init__()
        self.owner_id = owner_id
        self.content = content
        self.created = created or datetime.now()


class PosterSerializer(serializers.Serializer):
    owner_id = serializers.EmailField(default='default')
    content = serializers.CharField(max_length=200,default='SOME STRING')
    created = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Poster(**validated_data)

class PosterImage(models.Model):
    poster_id = models.IntegerField()
    image = models.ImageField()
