from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.get_accounts, name="get_accounts"),
    url('signup', views.signup, name='signup'),
    url('editprofile', views.edit, name='edit-profile'),
    url('delprofile', views.del_profile, name='delete-profile'),
    url('login', views.login, name='login'),
    url('validate_token', views.token_isvalid, name='validate_token'),
    url('change_profile', views.change_profile, name='change_profile'),
    url('suggestions', views.generate_suggestions, name='gen_suggestions')
]
