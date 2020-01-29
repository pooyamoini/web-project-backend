from django.conf.urls import url
from django.contrib import admin
from django.urls import  path

from . import views

urlpatterns = [
    path('follow' , views.follow , name = 'follow'),
    path('unfollow' , views.unfollow , name = 'unfollow') ,
    path('getFollowRelations' , views.get_follow_relations , name = 'getFollowRealations'),
]