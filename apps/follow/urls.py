from django.conf.urls import url
from django.contrib import admin
from django.urls import  path

from . import views

urlpatterns = [
    path('follow' , views.follow , name = 'follow'),
    path('unfollow' , views.unfollow , name = 'unfollow') ,
    path('getFollowRelations' , views.get_follow_relations , name = 'getFollowRealations'),
    path('get_single_relation' , views.get_single_relation , name = 'get_single_relation'),
    path('get_all_followings' , views.get_all_followings , name = 'get_all_following'),
    path('get_all_followers' , views.get_all_followers , name = 'get_all_followed'),
]