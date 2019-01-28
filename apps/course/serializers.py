from rest_framework import serializers
from apps.cms.models import CourseCategory,Course,CourseTeacher


class Categoryserializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('id', 'category')


class Teacherserializers(serializers.ModelSerializer):
    class Meta:
        model = CourseTeacher
        fields = ('id', 'name', 'info')


class Courseserializers(serializers.ModelSerializer):
    category = Categoryserializers()
    teacher = Teacherserializers()

    class Meta:
        model = Course
        fields =('id', 'title', 'teacher', 'category', 'cover', 'link', 'price', 'abstract', 'add_time')


