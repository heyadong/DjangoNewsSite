from django.db import models

# Create your models here.


# 新闻标签/分类
class NewsTag(models.Model):
    name = models.CharField(max_length=50,null=False)
    add_time = models.DateField(auto_now=True)


# 新闻
class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    thumbnail = models.URLField(max_length=800)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey('NewsTag',on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey("authdemo.User", on_delete=models.CASCADE)


# 轮播图

class Banners(models.Model):
    bannersimg = models.URLField(null=True)  # banners图片链接
    link_to = models.URLField(null=True)  # banners 跳转链接
    position = models.IntegerField()    # 优先级
    add_time = models.DateField(auto_now_add=True)  # 添加时间


# 课程模型
class Course(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey('CourseTeacher',on_delete=models.CASCADE)
    category = models.ForeignKey('CourseCategory',on_delete=models.CASCADE)
    link = models.URLField(null=False)
    times = models.CharField(max_length=20)
    cover = models.URLField(null=True)
    price = models.FloatField(null=True)
    abstract = models.TextField()       # 课程简介
    add_time = models.DateTimeField(auto_now_add=True)


# 课程分类
class CourseCategory(models.Model):
    category = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)


# 课程教师
class CourseTeacher(models.Model):
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=255)
    sex = models.CharField(max_length=20)  # 性别
    postion = models.CharField(max_length=100)  # 职位
    add_time = models.DateTimeField(auto_now_add=True)




