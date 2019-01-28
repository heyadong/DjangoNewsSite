from django import forms
from apps.forms import FormsMxin


class CommentForms(forms.Form,FormsMxin):
    content = forms.CharField(min_length=1,max_length=255,error_messages={'min_length':"评论不能为空",                                                                  'max_length':"评论超过最大字数255"})
    article = forms.CharField(max_length=100)




