from __future__ import unicode_literals

from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from pprint import pprint
from datetime import datetime
from base64 import b64decode
from django.core.files.base import ContentFile
from django_mysql.models import ListCharField

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
    image = models.ImageField(upload_to='images/%Y/%m/%d',default='/media/default/default_poster_image.jpg')
    tags =  ListCharField(
        base_field=models.CharField(max_length=10),
        size=20,
        max_length = 20*11,
        default='fashion'
    )

    @classmethod
    def create(cls, owner_id, content, image, tags, created=None):
        poster = cls(owner_id=owner_id,content=content,image=image,tags=tags,created=created or datetime.now())
        return poster

class PosterSerializer(serializers.Serializer):
    owner_id = serializers.EmailField(default='default')
    content = serializers.CharField(max_length=200,default='SOME STRING')
    created = serializers.DateTimeField(required=False)
    tags = serializers.ListField(
        child = serializers.CharField(max_length=10),
        min_length = 1,
        max_length = 20,
        required=True
    )

    # for post
    image_data = serializers.CharField(required=False)

    image_url = serializers.SerializerMethodField(required=False)

    def create(self, validated_data):
        image_data = b64decode(validated_data['image_data'])
        posterImage = ContentFile(image_data,'whatup.png')
        poster = Poster.create(owner_id=validated_data['owner_id'],content=validated_data['content'],image=posterImage,tags=validated_data['tags'])
        return poster

    def get_image_url(self, poster):
        if type(poster) is not Poster:
            return
        request = self.context.get('request')
        image_url = poster.image.url
        return request.build_absolute_uri(image_url)
