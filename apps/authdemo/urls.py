from django.urls import path
from .views import login_view,register_view
urlpatterns = [
    path('',login_view,name='loginview'),
    path('signup/',register_view,name='signup')
]