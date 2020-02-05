from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import Comment, RowComment, SubComment
from ..post.models import Post
from ..account.models import LoggInBasic, AccountBasic
from ..account.serializers import AccountSerializer
from .serializers import CommentSerializer, SubCommentSerializers, RowCommentSerializer
import string
import random
import datetime
import math


@csrf_exempt
@api_view(['POST'])
def get_comments(request):
    data = request.data
    if len(data.keys() & {'token', 'pid'}) >= 2:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(id_post=data['pid'])
            q = Comment.objects.get(pk=post.id_post)
            comments = q.comments
            comments_ser = SubCommentSerializers(comments, many=True)
            for x in comments_ser.data:
                x['account'] = RowComment.objects.get(
                    pk=x['main']).account.username
                x['src'] = RowComment.objects.get(pk=x['main']).account.profile
                x['main'] = RowComment.objects.get(pk=x['main']).content
            to_return = comments_ser.data
            for i in to_return:
                replies = []
                for c in i['replies']:
                    r = RowCommentSerializer(RowComment.objects.get(pk=c)).data
                    ac = AccountBasic.objects.get(pk=r['account'])
                    r['account'] = AccountSerializer(ac).data
                    replies.append(r)
                i['replies'] = replies
            return Response({'msg': to_return}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Post.DoesNotExist:
            return Response({'msg': 'invalid pid'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({'msg': []}, status.HTTP_200_OK)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def add_comment(request):
    data = request.data
    if len(data.keys() & {'token', 'content', 'pid'}) >= 3:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(id_post=data['pid'])
            try:
                q = Comment.objects.get(pk=post.id_post)
            except Comment.DoesNotExist:
                q = Comment(post=post.id_post)
                q.save()
            r = RowComment(
                account=account, content=data['content'])
            r.save()
            s = SubComment(main=r, cid=random.randrange(100000))
            s.save()
            q.comments.add(s)
            return Response({'msg': 'successfull'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Post.DoesNotExist:
            return Response({'msg': 'invalid pid'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def add_reply(request):
    data = request.data
    if len(data.keys() & {'token', 'pid', 'cid', 'content'}) >= 4:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(id_post=data['pid'])
            q = Comment.objects.get(pk=data['pid'])
            r = RowComment(
                account=account, content=data['content'])
            r.save()
            q.comments.get(cid=data['cid']).replies.add(r)
            q.save()
            return Response({'msg': 'successfull'}, status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'msg': 'comment not found'}, status.HTTP_406_NOT_ACCEPTABLE)
        except SubComment.DoesNotExist:
            return Response({'msg': 'invalid pid'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)