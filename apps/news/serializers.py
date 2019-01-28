from rest_framework import serializers
from .models import Comments
from apps.authdemo.serializers import UserSerializers
from apps.cms.serializers import ArticleSerialize


class Commentserialize(serializers.ModelSerializer):
    author = UserSerializers()
    # article = ArticleSerialize()
    class Meta:
        model = Comments
        fields = ('id','content','author','add_time')