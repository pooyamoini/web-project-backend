from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from ..account.models import AccountBasic
from ..account.serializers import AccountSerializer
from ..post.models import Post
from ..account.models import LoggInBasic
from ..post.serializers import PostSerializer
from ..account_generic.models import AccountGeneric

from ..notification.models import Notification
from ..notification.models import Follows
from ..notification.models import Comments
from ..notification.models import Like
from ..notification.models import Dislike
from ..notification.serializers import NotifSerializer
from ..notification.serializers import FollowsSerializer
from ..notification.serializers import CommentsSerializer
from ..notification.serializers import LikeSerializer
from ..notification.serializers import DislikeSerializer

import string
import random
import datetime
import math


@csrf_exempt
@api_view(['POST'])
def index(request):
    data = request.data
    res = {}
    follows = []
    comments = []
    likes = []
    dislikes = []
    account = LoggInBasic.objects.get(token= data["token"]).account
    # account = AccountBasic.objects.get(pk=data['username'])
    account_generic = AccountGeneric.objects.get(pk=account)
    for i in account_generic.followers.all():
        follows.append(i)
    follows = AccountSerializer(follows, many=True).data
    res['follows'] = follows

    for i in account_generic.posts.all():
        for j in i.nlikes.all():
            if j == account : continue
            likes.append({'account': AccountSerializer(j).data, 'post': PostSerializer(i).data})
        for j in i.ndislikes.all():
            if j == account : continue
            dislikes.append({'account': AccountSerializer(j).data, 'post': PostSerializer(i).data})
    res["likes"] = likes
    res['dislikes'] = dislikes

    return Response({'msg': res})
