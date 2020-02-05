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
from ..comment.models import Comment
from ..comment.serializers import CommentSerializer
from ..Numbers.models import Number
from .serializers import PostSerializer
import string
import random
import datetime
import math


def add_number():
    n = Number.objects.all()[0]
    n.value += 1
    n.save()


@csrf_exempt
@api_view(['POST'])
def create_post(request):
    data = request.data
    if len(data.keys() & {'content', 'image', 'token'}) >= 3:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            if len(Number.objects.all()) == 0:
                n = Number(name=1, value=0)
                n.save()
            id_post = Number.objects.all()[0].value
            add_number()
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
            return Response({'msg': {'post': post_serializer.data, 'account': account_serializer.data, 'isliked': is_liked,
                                     'isDisliked': is_disliked, 'date': date}}, status.HTTP_200_OK)
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
            date = post.date_post
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
            post.date_post = date
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
                    posts.append(return_serializer(i, a, date, 1))
            for i in AccountGeneric.objects.get(account=my_account).posts.all():
                date = get_correct_time(time=i.date_post)
                posts.append(return_serializer(i, my_account, date, 0))
            suggests = get_suggestions(token=data['token'])
            return Response({'msg': {'posts': get_sorted_posts(posts), 'header': suggests}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Post.DoesNotExist:
            return Response({'msg': {'posts': [], 'header': []}}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_homepage_news(request):
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
                    posts.append(return_serializer(i, a, date, 1))
            for i in AccountGeneric.objects.get(account=my_account).posts.all():
                date = get_correct_time(time=i.date_post)
                posts.append(return_serializer(i, my_account, date, 0))
            suggests = get_suggestions(token=data['token'])
            return Response({'msg': {'posts': get_new_posts(posts), 'header': suggests}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_homepag_hots(request):
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
                    posts.append(return_serializer(i, a, date, 1))
            for i in AccountGeneric.objects.get(account=my_account).posts.all():
                date = get_correct_time(time=i.date_post)
                posts.append(return_serializer(i, my_account, date, 0))
            posts = sorted(posts, key=lambda k: -k['likes'])
            suggests = get_suggestions(token=data['token'])
            return Response({'msg': {'posts': posts, 'header': suggests}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
@api_view(['POST'])
def get_homepage_interest(request):
    data = request.data
    if len(data.keys() & {'token'}) >= 1:
        try:
            my_account = LoggInBasic.objects.get(token=data['token']).account
            posts = get_interest_posts(my_account)
            suggests = get_suggestions(token=data['token'])
            return Response({'msg': {'posts': posts, 'header': suggests}}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


def get_interest_posts(my_account):
    posts = []
    for c in Comment.objects.all():
        for x in c.comments.all():
            if x.main.account.username == my_account.username:
                p = Post.objects.get(pk=c.post)
                date = get_correct_time(time=p.date_post)
                account = p.account
                if not any(d['id'] == p.id_post for d in posts):
                    posts.append(return_serializer(
                        p, account, date, 1))
            for z in x.replies.all():
                if z.account.username == my_account.username:
                    p = Post.objects.get(pk=c.post)
                    date = get_correct_time(time=p.date_post)
                    account = p.account
                    if not any(d['id'] == p.id_post for d in posts):
                        posts.append(return_serializer(
                            p, account, date, 1))
    return posts


def return_serializer(post, account, date, type_ser=1):
    title = account.username if type_ser == 0 else post.account.username
    return {'title': account.username, 'content': post.content,
            'image': post.image, 'date': date, 'name': account.name, 'username': account.username, 'profile': account.profile,
            'id': post.id_post, 'likes': len(post.nlikes.all()), 'dislikes': len(post.ndislikes.all()), 'realtime': return_delta_time(post.date_post)}


def get_suggestions(token):
    random_post_following = get_random_following(token)
    random_post_hot = get_random_hots()
    random_post_new = get_random_new()
    random_post_interest = get_random_interest(token)
    return {'hot': random_post_hot, 'new': random_post_new, 'follow': random_post_following, 'interest': random_post_interest}


def get_random_following(token):
    my_account = LoggInBasic.objects.get(token=token).account
    followings = AccountGeneric.objects.get(pk=my_account).followings
    followings_serializer = AccountSerializer(followings, many=True)
    if len(followings.all()) == 0:
        return {}
    random_following = followings.all(
    )[random.randrange(len(followings.all()))]
    random_posts = AccountGeneric.objects.get(
        account=random_following).posts.all()
    if len(random_posts) == 0:
        return {}
    random_following_post = random_posts[random.randrange(len(random_posts))]
    return(PostSerializer(random_following_post).data)


def get_random_hots():
    posts = PostSerializer(Post.objects.all(), many=True).data
    if len(posts) == 0:
        return {}
    sorted_posts = sorted(posts, key=lambda k: -len(k['nlikes']))
    post = sorted_posts[random.randrange(min(3, len(posts)))]
    return post


def get_random_new():
    if len(Post.objects.all()) == 0:
        return {}
    posts = PostSerializer(Post.objects.all().order_by(
        '-date_post'), many=True).data
    post = Post.objects.get(
        pk=posts[random.randrange(min(5, len(posts)))]['id_post'])
    return PostSerializer(post).data


def get_random_interest(token):
    my_account = LoggInBasic.objects.get(token=token).account
    posts = get_interest_posts(my_account)
    if len(posts) == 0:
        return {}
    post = Post.objects.get(pk=posts[random.randrange(len(posts))]["id"])
    return PostSerializer(post).data


def get_new_posts(posts):
    to_return = []
    for i in posts:
        if i['realtime'] >= 2 * 3600:
            continue
        to_return.append(i)
    return sorted(to_return, key=lambda k: k['realtime'])


def get_sorted_posts(posts):
    return sorted(posts, key=lambda k: k['realtime'])


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


@csrf_exempt
@api_view(['POST'])
def edit_post(request):
    data = request.data
    if len(data.keys() & {'content', 'pid', 'token'}) >= 3:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(pk=data['pid'])
            date = post.date_post
            post.content = data['content']
            post.date_post = date
            post.save()
            return Response({'msg': 'post successfully edited'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def delete_post(request):
    data = request.data
    if len(data.keys() & {'token', 'pid'}) >= 2:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            post = Post.objects.get(pk=data['pid'])
            date = post.date_post
            if post.account.username == account.username:
                add_number()
                post.delete()
                return Response({'msg': 'post successfully deleted'}, status.HTTP_200_OK)
            return Response({'msg': 'not your post'}, status.HTTP_406_NOT_ACCEPTABLE)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except Post.DoesNotExist:
            return Response({'msg': 'invalid pid'}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return Response({'msg': content}, status.HTTP_406_NOT_ACCEPTABLE)
