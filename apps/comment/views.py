from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from apps.account.models import AccountBasic 
from .models import Comment
from .serilizer import CommentSerializer

@csrf_exempt
@api_view(['GET'])
def get_all_comments(request):
    data = request.data
    serializer = CommentSerializer(data = data)
    if serializer.is_valid():
        #chech if the post is valid#
        comments = Comment.objects.filter(post_id = data['post_id'])
        comments.sort(key = lambda x:x['creation_time'] , reverse = True)
        serializer = CommentSerializer(comments , many = True)
        return JsonResponse(comments.data , safe= False)
    else:
        return responseGenerator('Invalid Request' , 406)




@csrf_exempt
@api_view(['POST'])
def comment(request):
    data = request.data
    ans = comment_mutual(data)
    #check if post is valid

    if type(ans) == Response:
        return ans
    return responseGenerator(ans.validated_data , 200)
    if comment_exists(data['id']):
        return responseGenerator('Comment id already exists' , 406)
    serializer = ans
    serializer.save()
    return responseGenerator('Comment Created' , 200)

@csrf_exempt
@api_view(['POST'])
def delete_comment(request):
    data = request.data
    ans = comment_mutual(data)
    #check if post is valid

    if type(ans) == Response:
        return ans
    if not comment_exists(data['id']):
        return responseGenerator('Comment does not exist' , 406)
    Comment.objects.delete(id = data['id'])    

@csrf_exempt
@api_view(['POST'])
def edit_comment(request):
    data = request.data
    ans =  comment_mutual(data)
    #check if post is valid
    if type(ans) == Response:
        return ans
    return responseGenerator('jooon' , 1)
    if not comment_exists(data['id']):
        return responseGenerator('Comment does not exist' , 406)
    instance =  Comment.objects.get(id = data['id'])
    instance.comment = validated_data.get('comment' , instance.comment)
    instance.edited_time = datetime.now
    instance.image_name = validated_data('image_name', instance.image_name)
    instance.save()
    return responseGeneryator('Comment Edited Successfully' , 200)


def comment_exists(comment_id):
    try:
        Comment.objects.get(id = comment_id)
        return True
    except Comment.DoesNotExist:
        return False   


def comment_mutual(data):
    serializer = CommentSerializer(data = data)
    if serializer.is_valid():
        creator_id = data['creator_id']
        if not is_id_in_accounts(creator_id):
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
