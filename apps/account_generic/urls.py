from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^(?P<username>\w{0,50})/$', views.test, name='test')
]
