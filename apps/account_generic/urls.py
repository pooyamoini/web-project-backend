from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^get/(?P<username>\w{0,50})/$',
        views.get_profile, name='get_profile'),
    url('follow/', views.follow, name='follow'),
]
