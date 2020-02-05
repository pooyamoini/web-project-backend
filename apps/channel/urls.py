from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.get_channels, name="get_channels"),
    url('create', views.create_channel, name="create_channel"),
    url(r'^add_member/$', views.add_member, name="add_member"),
    url(r'^remove_member/$', views.remove_member, name="remove_member"),
    url(r'^create_post/$', views.create_post, name="create_post"),

]
