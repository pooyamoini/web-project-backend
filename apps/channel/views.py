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
from ..channel.models import Channel
from ..channel.serializers import ChannelSerializer
from ..Numbers.models import Number


import string
import random
import datetime
import math

@csrf_exempt
def get_channels(request):
    """
    List all channels
    """
    channels = Channel.objects.all()
    return JsonResponse(ChannelSerializer(channels, many=True).data, safe=False)


@csrf_exempt
@api_view(['POST'])
def create_channel(request):
    data = request.data
    if len(data.keys() & {'name', 'bio', 'rules', 'token'}) >= 4:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            name = data['name']
            bio = data['bio']
            rules = data['rules']
            channel = Channel(name=name, bio=bio, rules=rules, admin=account)
            channel.save()

            return Response({'msg': 'channel successfully created'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'Not valid Data'}, status.HTTP_406_NOT_ACCEPTABLE)

@csrf_exempt
@api_view(['POST'])
def add_member(request):
    data = request.data
    if len(data.keys() & {'username', 'channel_name','token'}) >= 3:
        try:
            saccount = LoggInBasic.objects.get(token=data['token']).account
            taccount = AccountBasic.objects.get(pk=data['username'])
            channel = Channel.objects.get(pk=data['channel_name'])
            if channel.admin != saccount:
                return Response({'msg': 'you are not admin'}, status.HTTP_406_NOT_ACCEPTABLE)
            channel.members.add(taccount)
            channel.save()
            return Response({'msg': 'member succesfully added'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'Not valid Data'}, status.HTTP_406_NOT_ACCEPTABLE)

@csrf_exempt
@api_view(['POST'])
def remove_member(request):
    data = request.data
    if len(data.keys() & {'username', 'channel_name','token'}) >= 3:
        try:
            saccount = LoggInBasic.objects.get(token=data['token']).account
            taccount = AccountBasic.objects.get(pk=data['username'])
            channel = Channel.objects.get(pk=data['channel_name'])
            if channel.admin != saccount:
                return Response({'msg': 'you are not admin'}, status.HTTP_406_NOT_ACCEPTABLE)
            channel.members.remove(taccount)
            channel.save()
            return Response({'msg': 'member succesfully removed'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'Not valid Data'}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def create_post(request):
    data = request.data
    if len(data.keys() & {'content', 'image', 'channel_name', 'token'}) >= 4:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            if len(Number.objects.all()) == 0:
                n = Number(name=1, value=0)
                n.save()
            channel = Channel.objects.get(pk=data['channel_name'])
            id_post = Number.objects.all()[0].value
            add_number()
            time_now = datetime.datetime.now()
            content = data['content']
            image = data['image']
            post = Post(account=account, id_post=id_post,
                        date_post=time_now, content=content, image=image)
            post.save()
            channel.posts.add(post)
            channel.save()
            return Response({'msg': 'post successfully created'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)

def add_number():
    n = Number.objects.all()[0]
    n.value += 1
    n.save()
