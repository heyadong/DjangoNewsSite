from django.urls import path
from apps.news.views import news_detail,search,draw_example,sms_send,newslist,comment_list,news_comment
app_name = 'news'
urlpatterns = [
    # path('course_detail', course_detail),
    # path('course_live', course_live),
    path('search', search),
    path('<int:news_id>',news_detail, name='news_detail'),
    path('draw',draw_example,name='captcha_draw'),
    path('sms',sms_send),
    path('newslist/',newslist),
    path('newscomment/',news_comment),
    path('comment_list/',comment_list)
]