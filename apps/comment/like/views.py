from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from apps.account.models import AccountBasic 
from apps.comment.models import Comment
from .models import Like 
from apps.comment.serilizer import CommentSerializer
from .serializer import LikeSerializer
from _datetime import datetime

@csrf_exempt
@api_view(['GET'])
def get_all_likes(request):
    return get_likes_dislikes(request , True)

@csrf_exempt
@api_view(['GET'])
def get_all_dislikes(request):
    return get_likes_dislikes(request , False)


def get_likes_dislikes(request , is_like):
    data = request.data
    serializer = CommentSerializer(data = data)
    if serializer.is_valid():
        try:
            comment_id = data['id']
            likes = Like.objects.filter(comment_id = comment_id , is_like = is_like)
            serializer = LikeSerializer(likes , many = True)
            return JsonResponse(serializer.data , safe= False)
        except Comment.DoesNotExist :
            return responseGenerator('Invalid Request' , 406)
    return responseGenerator("Invalid Input", 406)


@csrf_exempt
@api_view(['POST'])
def like(request):
    data = request.data
    ans = like_mutual(data)
    if type(ans) == Response :
        return ans
    serializer = ans
    if not comment_exists(data['comment_id']):
        return responseGenerator('Invalid Comment' , 406)
    comment = Comment.objects.get(pk = data['comment_id'])
    try:
        like =  Like.objects.filter(comment_id = data['comment_id'] , liker_id = data['liker_id']) 
        like = like[0]
        if not like.is_like == serializer.validated_data['is_like']:
            if like.is_like:
                comment.like_counter -= 1
                comment.dislike_counter += 1
            else:
                comment.like_counter += 1
                comment.dislike_counter -= 1
            like.is_like = not like.is_like
            comment.save()
            like.save()    
        return responseGenerator("You voted Successfully" , 200)    
    except IndexError:
        if serializer.validated_data['is_like']:
            comment.like_counter += 1
        else:
            comment.dislike_counter +=  1
        comment.save()
        serializer.save()
        return responseGenerator('You voted' , 200)



@csrf_exempt
@api_view(['POST'])
def unlike(request):
    data = request.data
    ans = like_mutual(data)
    if(type(ans) == Response):
        return ans
    if not comment_exists(data['comment_id']):
        return responseGenerator('Invalid Comment', 406)

    try:
        likes =  Like.objects.filter(comment_id = data['comment_id'], liker_id = data['liker_id'])
        like = likes[0]
    except IndexError:
        return responseGenerator('You have not voted on this post' , 406)
    comment = Comment.objects.get(pk = data['comment_id'])
    if like.is_like:
        comment.like_counter -= 1
    else:
        comment.dislike_counter -= 1
    like.delete()
    comment.save()
    return responseGenerator('You got back your vote' , 200)



def comment_exists(comment_id):
    try:
        Comment.objects.get(id = comment_id)
        return True
    except Comment.DoesNotExist:
        return False   


def like_mutual(data):
    serializer = LikeSerializer(data = data)
    if serializer.is_valid():
        liker_id = data['liker_id']
        if not is_id_in_accounts(liker_id):
            return responseGenerator('Invalid Creator' , 406)
        else:  
            return serializer
    else:
        return responseGenerator('Invalid Input', 406)


def is_id_in_accounts(account_id):
    try:
        account = AccountBasic.objects.get(pk = account_id)
        return True
    except AccountBasic.DoesNotExist:
        return False


def responseGenerator(msg , statusType):
    statusT = status.HTTP_200_OK
    if statusType == 406:
        statusT = status.HTTP_406_NOT_ACCEPTABLE
    return Response({'msg':msg}, statusT)
