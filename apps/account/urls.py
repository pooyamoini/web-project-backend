from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.get_accounts, name="get_accounts"),
    url(r'^test', views.sample_test, name="test"),
]
