from django import forms
from apps.forms import FormsMxin
from .models import Article, Banners,Course


class TagForm(forms.Form):
    tag = forms.CharField(required=True, error_messages={'required': "添加的标签不能为空"})


class TagForm2(forms.Form):
    id = forms.IntegerField(required=True)
    tag = forms.CharField(required=True, error_messages={'required': "添加的标签不能为空"})


class ArticleForm(forms.ModelForm, FormsMxin):
    tag = forms.IntegerField()

    class Meta:
        model = Article
        exclude = ["tag", "pub_time", "author"]


class BannerForm(forms.ModelForm,FormsMxin):
    class Meta:
        model = Banners
        exclude = ['add_time']


class CourseForm(forms.ModelForm, FormsMxin):
    category = forms.IntegerField()
    teacher = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ['add_time', 'category', 'teacher']

class TeacherForm(forms.Form):
    name = forms.CharField(max_length=100),


class CourseCategoryForm(forms.Form,FormsMxin):
    category = forms.CharField(min_length=1, max_length=50, error_messages={
        'max_length': "输入课程分类最多50字",
        'min_length': "请输入课程分类"
    })
