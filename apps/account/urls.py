from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    url(r'^$', views.get_accounts, name="get_accounts"),
    url('signup', views.signup, name='signup'),
    path('follow/' , include('apps.follow.urls')),
]
