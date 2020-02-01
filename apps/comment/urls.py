from django.conf.urls import url
from django.contrib import admin
from django.urls import include , path
from . import views

urlpatterns = [
    path('comment' , views.comment),
    path('delete' , views.delete_comment),
    path('edit' , views.edit_comment),
    path('get_comments' , views.get_all_comments),  
    path('like/', include('apps.comment.like.urls')),  
]
