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
from ..post.serializers import PostSerializer
import string
import random
import datetime
import math


def get_accounts(name):
    res = []
    for i in AccountBasic.objects.all():
        if(name in i.name.lower() or name in i.username.lower()):
            res.append(i)
    return AccountSerializer(res, many=True).data

def get_posts(name):
    res = []
    for i in Post.objects.all():
        if(name in i.content):
            res.append(i)
    res = PostSerializer(res, many=True).data 

    
    for i in res :
        name = i['account']
        account = AccountBasic.objects.get(pk = name)
        i["account"] = AccountSerializer(account).data

        # dseconds = (datetime.datetime.now(
        #         datetime.timezone.utc) - i["date_post"]).seconds
        # date = 'Just know'
        # if dseconds > 60 and dseconds <= 3600:
        #     date = str(math.floor(dseconds/60)) + ' mins ago'
        # elif dseconds > 3600:
        #     date = str(math.floor(dseconds / 3600)) + ' hours age'
        # i['date_post'] = date

    return res        
        

@csrf_exempt
@api_view(['POST'])
def index(request):
    data = request.data
    return Response({'msg': { 'accounts': get_accounts(data["name"].lower()), 'posts': get_posts(data['name'].lower()), 'channels': [] }} )
