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
            return Response({'msg': {'post': post_serializer.data, 'account': account_serializer.data, 'isliked': is_liked, 'isDisliked': is_disliked}}, status.HTTP_200_OK)
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
