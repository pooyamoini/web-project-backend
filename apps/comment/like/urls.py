from django.conf.urls import url
from django.contrib import admin
from django.urls import  path
from . import views

urlpatterns = [
    path('like' , views.like , name  = 'like'),
    path('unlike' , views.unlike , name = 'unlike'),
    path('get_likes' , views.get_all_likes , name = 'get_likes'),
    path('get_dislikes' , views.get_all_dislikes , name = 'get_dislikes'),
]
