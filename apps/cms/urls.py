from django.urls import path
from .views import cms_login,cms_index,CmsNews,NewsCategory,Newslist,tag_delete,tag_edit,banners,upload,bannersdelete
from apps.cms import course_view
app_name = 'cms'
urlpatterns = [
    path('login', cms_login, name='login'),
    path('index', cms_index, name='cmsindex'),
    path('news/', CmsNews.as_view(), name='news'),
    path('newstag', NewsCategory.as_view(), name='category'),
    path('newsquery/', Newslist.as_view(), name='newsquery'),
    path('tag_delete/<int:id>', tag_delete, name="tag_delete"),
    path("tag_edit/", tag_edit, name="tag_edit"),
    path('banner/', banners, name='banners'),
    path('banner_delete/', bannersdelete, name='banners_delete'),
    path('upload/', upload, name='upload')
]


# 课程发布页urls
urlpatterns += [
    path('course/', course_view.CourseView.as_view(), name='course'),
    path('course/delete/', course_view.course_delete, name='course_delete'),
    path('course/list/', course_view.CourseList.as_view(), name="course_list"),
    path('teacher/', course_view.TeacherAdd.as_view(), name="teacher"),
    path('course_category/', course_view.CourseTag.as_view(), name="course_category"),
    path('course_category/del/', course_view.coursecategory_del, name="category_del"),
    path('course_category/edit/', course_view.coursecategory_edit, name="category_edit")
]