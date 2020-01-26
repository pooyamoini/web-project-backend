from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url('', views.get_accounts, name="get_accounts"),
]
