from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


from . import views


urlpatterns = [
    path('api/account/', include('apps.account.urls')),
    path('api/comment/', include('apps.comment.urls')),
]
