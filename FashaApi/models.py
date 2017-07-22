from __future__ import unicode_literals

from django.db import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from pprint import pprint
from datetime import datetime
from base64 import b64decode
from django.core.files.base import ContentFile

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

    @classmethod
    def create(cls, owner_id, content, image, created=None):
        poster = cls(owner_id=owner_id,content=content,image=image,created=created or datetime.now())
        return poster

class PosterSerializer(serializers.Serializer):
    owner_id = serializers.EmailField(default='default')
    content = serializers.CharField(max_length=200,default='SOME STRING')
    created = serializers.DateTimeField(required=False)

    # for post
    image_data = serializers.CharField(required=False)

    image_url = serializers.SerializerMethodField()
    def create(self, validated_data):
        poster = None
        image_data = b64decode(validated_data['image_data'])
        pprint(vars(validated_data))
        if image_data is not None:
            posterImage = ContentFile(image_data,'whatup.png')
            poster = Poster.create(owner_id=validated_data['owner_id'],content=validated_data['content'],image=posterImage)
        else:
            poster = Poster.create(**validated_data)
        return poster

    def get_image_url(self, poster):
        request = self.context.get('request')
        image_url = poster.image.url
        return request.build_absolute_uri(image_url)
