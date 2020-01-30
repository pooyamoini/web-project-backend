from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


from . import views


urlpatterns = [
    path('api/account/', include('apps.account.urls')),
    path('api/post', include('apps.post.urls'))
]
