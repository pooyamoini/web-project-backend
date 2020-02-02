from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Post
from ..account.models import LoggInBasic, AccountBasic
from ..account.serializers import AccountSerializer
from ..account_generic.models import AccountGeneric
from .serializers import PostSerializer
import string
import random
import datetime
import math


@csrf_exempt
@api_view(['POST'])
def create_post(request):
    data = request.data
    if len(data.keys() & {'content', 'image', 'token'}) >= 3:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            id_post = len(Post.objects.all())
            time_now = datetime.datetime.now()
            content = data['content']
            image = data['image']
            post = Post(account=account, id_post=id_post,
                        date_post=time_now, content=content, image=image)
            account_gen = AccountGeneric.objects.get(pk=account)
            post.save()
            account_gen.posts.add(post)
            account_gen.save()
            return Response({'msg': 'post successfully created'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_post(request, post_id):
    data = request.data
    if len(data.keys() & {'token'}) >= 1:
        try:
            my_account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(pk=post_id)
            post_serializer = PostSerializer(post)
            account = post.account
            account_serializer = AccountSerializer(account)
            is_liked = post.nlikes.filter(
                username=my_account.username).exists()
            is_disliked = post.ndislikes.filter(
                username=my_account.username).exists()
            dseconds = (datetime.datetime.now(
                datetime.timezone.utc) - post.date_post).seconds
            date = 'Just know'
            if dseconds > 60 and dseconds <= 3600:
                date = str(math.floor(dseconds/60)) + ' mins ago'
            elif dseconds > 3600:
                date = str(math.floor(dseconds / 3600)) + ' hours age'
            return Response({'msg': {'post': post_serializer.data, 'account': account_serializer.data, 'isliked': is_liked, 'isDisliked': is_disliked, 'date': date}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Post.DoesNotExist:
            return Response({'msg': 'invalid pid'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def like_dislike(request):
    data = request.data
    if len(data.keys() & {'token', 'type', 'post_id'}) >= 1:
        try:
            my_account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(pk=data['post_id'])
            if data['type'] == 'like':
                if post.nlikes.filter(username=my_account.username).exists():
                    post.nlikes.remove(my_account)
                else:
                    post.nlikes.add(my_account)
            else:
                if post.ndislikes.filter(username=my_account.username):
                    post.ndislikes.remove(my_account)
                else:
                    post.ndislikes.add(my_account)
            post.save()
            return Response({'msg': 'successfull'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Post.DoesNotExist:
            return Response({'msg': 'invalid pid'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_homepage(request):
    data = request.data
    if len(data.keys() & {'token'}) >= 1:
        try:
            my_account = LoggInBasic.objects.get(token=data['token']).account
            followings = AccountGeneric.objects.get(pk=my_account).followings
            followings_serializer = AccountSerializer(followings, many=True)
            posts = []
            accounts = []
            for a in followings.all():
                gen_a = AccountGeneric.objects.get(account=a)
                for i in gen_a.posts.all():
                    date = get_correct_time(time=i.date_post)
                    posts.append({'title': i.account.username, 'content': i.content,
                                  'image': i.image, 'date': date, 'name': a.name, 'username': a.username, 'profile': a.profile,
                                  'id': i.id_post, 'likes': len(i.nlikes.all()), 'dislikes': len(i.ndislikes.all())})
            for i in AccountGeneric.objects.get(account=my_account).posts.all():
                date = get_correct_time(time=i.date_post)
                posts.append({'title': my_account.username, 'content': i.content,
                              'image': i.image, 'date': date, 'name': my_account.name, 'username': my_account.username, 'profile': my_account.profile,
                              'id': i.id_post, 'likes': len(i.nlikes.all()), 'dislikes': len(i.ndislikes.all())})
            return Response({'msg': {'posts': posts}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


def get_correct_time(time):
    dseconds = (datetime.datetime.now(
        datetime.timezone.utc) - time).seconds
    date = 'Just know'
    if dseconds > 60 and dseconds <= 3600:
        date = str(math.floor(dseconds/60)) + ' mins ago'
    elif dseconds > 3600:
        date = str(math.floor(dseconds / 3600)) + ' hours age'
    return(date)
