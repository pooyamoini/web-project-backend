from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
import string
import random
import datetime
import math
from .models import AccountGeneric
from .serializers import AccountGenericSerializer
from ..account.models import LoggInBasic, AccountBasic
from ..account.serializers import AccountSerializer
from ..post.serializers import PostSerializer


@csrf_exempt
@api_view(['POST'])
def get_profile(request, username):
    data = request.data
    if len(data.keys() & {'token'}) >= 1:
        token = request.data['token']
        try:
            my_account = LoggInBasic.objects.get(token=token).account
            account = AccountBasic.objects.get(pk=username)
            account_generic = AccountGeneric.objects.get(pk=account)
            is_followed = account_generic.followers.filter(
                name=my_account.name).exists()
            data = {'name': account.name,
                    'username': username, 'bio': account.bio, 'nfollowers': account_generic.followers.count(), 'nfollowings': account_generic.followings.count(), 'npost': account_generic.posts.count(), 'profile': account.profile, 'isfollowed': is_followed}
            return Response({'msg': data}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid username'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def follow(request):
    data = request.data
    if len(data.keys() & {'token', 'username'}) >= 2:
        token = request.data['token']
        try:
            username = data['username']
            my_account = LoggInBasic.objects.get(token=token).account
            account = AccountBasic.objects.get(pk=username)
            account_generic = AccountGeneric.objects.get(pk=account)
            my_account_generic = AccountGeneric.objects.get(pk=my_account)
            if (account_generic.followers.filter(username=my_account.username).exists()):
                account_generic.followers.remove(my_account)
                my_account_generic.followings.remove(account)
                account_generic.save()
                my_account_generic.save()
                return Response({'msg': 'successfully removed'}, status.HTTP_200_OK)
            my_account_generic.followings.add(account)
            account_generic.followers.add(my_account)
            account_generic.save()
            my_account_generic.save()
            return Response({'msg': 'successfully added'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid username'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_followers_followings(request):
    data = request.data
    if len(data.keys() & {'token', 'username'}) >= 2:
        token = request.data['token']
        try:
            username = data['username']
            my_account = LoggInBasic.objects.get(token=token).account
            account = AccountBasic.objects.get(pk=username)
            account_generic = AccountGeneric.objects.get(pk=account)
            my_account_generic = AccountGeneric.objects.get(pk=my_account)
            followers = AccountSerializer(account_generic.followers, many=True)
            followings = AccountSerializer(
                account_generic.followings, many=True)
            return Response({'msg': {'followers': followers.data, 'followings': followings.data}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid username'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_posts_username(request):
    data = request.data
    if len(data.keys() & {'token', 'username'}) >= 2:
        token = request.data['token']
        try:
            username = data['username']
            my_account = LoggInBasic.objects.get(token=token).account
            account = AccountBasic.objects.get(pk=username)
            account_generic = AccountGeneric.objects.get(pk=account)
            my_account_generic = AccountGeneric.objects.get(pk=my_account)
            posts = account_generic.posts
            dates = []
            for p in posts.all():
                dates.append(get_correct_time(p.date_post))
            return Response({'msg': {'posts': PostSerializer(posts, many=True).data, 'date': dates}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid username'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)


def return_delta_time(time):
    return (datetime.datetime.now(datetime.timezone.utc) - time).seconds


def get_correct_time(time):
    dseconds = return_delta_time(time)
    date = 'Just know'
    if dseconds > 60 and dseconds <= 3600:
        date = str(math.floor(dseconds/60)) + ' mins ago'
    elif dseconds > 3600:
        date = str(math.floor(dseconds / 3600)) + ' hours age'
    return(date)
