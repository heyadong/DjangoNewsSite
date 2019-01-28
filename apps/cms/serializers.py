from rest_framework import serializers
from .models import NewsTag,Article
from apps.authdemo.serializers import UserSerializers


class TagSerialize(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ('id','name')


class ArticleSerialize(serializers.ModelSerializer):
    author = UserSerializers()
    tag = TagSerialize()

    class Meta:
        model = Article
        fields = ('id','title','description','thumbnail','pub_time','tag','author')