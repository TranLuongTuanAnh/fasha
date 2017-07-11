from __future__ import unicode_literals

from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from pprint import pprint

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
    def __init__(self, owner_mail, content, created=None):
        self.owner_id = owner_id
        self.content = content
        self.created = created or datetime.now()

class PosterSerializer(serializers.Serializer):
    owner_id = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Poster(**validated_data)
