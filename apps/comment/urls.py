from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url('add/', views.add_comment, name="add_comments"),
    url('get/', views.get_comments, name="get"),
    url('reply/', views.add_reply, name="reply")
]
