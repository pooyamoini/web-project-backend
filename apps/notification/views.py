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

from ..notification.models import Notification, Follows, Comments, Like, Dislike
from ..notification.serializers import NotifSerializer, FollowsSerializer, CommentsSerializer, LikeSerializer, DislikeSerializer

from ..comment.models import Comment, RowComment, SubComment

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
    likes = []
    dislikes = []
    account = LoggInBasic.objects.get(token=data["token"]).account
    account_generic = AccountGeneric.objects.get(pk=account)
    follows = AccountSerializer(
        account_generic.followers.all(), many=True).data
    res['follows'] = follows

    for i in account_generic.posts.all():
        for j in i.nlikes.all():
            if j == account:
                continue
            likes.append({'account': AccountSerializer(
                j).data, 'post': PostSerializer(i).data})
        for j in i.ndislikes.all():
            if j == account:
                continue
            dislikes.append({'account': AccountSerializer(
                j).data, 'post': PostSerializer(i).data})
    res["likes"] = likes
    res['dislikes'] = dislikes
    res["comments"] = get_comment(account)
    return Response({'msg': res})


def get_comment(account):
    comments = []
    for i in AccountGeneric.objects.get(pk=account).posts.all():
        try:
            c = Comment.objects.get(post=i.id_post)
            for s in c.comments.all():
                if s.main.account == account:
                    continue
                comments.append({'account': AccountSerializer(
                    s.main.account).data, 'post': PostSerializer(i).data})
                for j in s.replies.all():
                    if j.account == account:
                        continue
                    comments.append({'account': AccountSerializer(
                        j.account).data, 'post': PostSerializer(i).data})
        except:
            return []
    return comments