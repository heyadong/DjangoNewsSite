from django.urls import path
from apps.course import views
app_name = "course"
urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course_res/', views.course_asny, name='course_res')
]