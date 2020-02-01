from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^(?P<username>\w{0,50})/$', views.get_profile, name='get_profile'),
]
