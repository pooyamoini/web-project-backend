from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url('create', views.create_post, name="create_post"),
    url(r'^get/(?P<post_id>\w{0,50})/$', views.get_post, name='get_pid'),
    url(r'^like/$', views.like_dislike, name='like'),
    url(r'^homepage/$', views.get_homepage, name='homepage'),
    url(r'^homepage/news/$', views.get_homepage_news, name='news'),
    url(r'^homepage/hots/$', views.get_homepag_hots, name="hots"),
    url(r'^editpost/$', views.edit_post, name='edit'),
    url(r'^delete/$', views.delete_post, name="delete")
]
