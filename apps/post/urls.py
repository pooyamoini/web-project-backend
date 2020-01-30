from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url('create', views.create_post, name="create_post"),
]
