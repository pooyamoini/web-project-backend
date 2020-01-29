from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from apps.account.models import AccountBasic 
from .models import AccountFollowType
from .serializer import AccountFollowTypeSerializer

@csrf_exempt
@api_view(['GET'])
def get_follow_relations(request):
    """
    list all follow relations
    """
    accounts = AccountFollowType.objects.all()
    account_serializer = AccountFollowTypeSerializer(accounts, many=True)
    return JsonResponse(account_serializer.data, safe=False)


@csrf_exempt
@api_view(['POST'])
def follow(request):
    """
    make a follow realtions
    """
    pass
    data = request.data
    ans = follow_and_unfollow_mutual(data)
    if type(ans) == Response:
        return ans
    serializer = ans        
    try:
        account = AccountFollowType.objects.get(follower_id = data['follower_id'] , followed_id = data['followed_id'])
        return responseGenerator('Already Followed' , 406)
    except AccountFollowType.DoesNotExist:
        serializer.save()
        return responseGenerator('Successfull follow' , 200)


@csrf_exempt
@api_view(['POST'])
def unfollow(request):
    """
    make a unfollow realtions
    """
    data = request.data
    ans = follow_and_unfollow_mutual(data)
    if type(ans) == Response:
        return ans
    serializer = ans
    try:
        relation = AccountFollowType.objects.get(follower_id = data['follower_id'] , followed_id = data['followed_id'])
        relation.delete()
        return responseGenerator('Successfull unfollow' , 200)
    except AccountFollowType.DoesNotExist:
        return responseGenerator('There is no such relation' , 406)


def follow_and_unfollow_mutual(data):
    serializer = AccountFollowTypeSerializer(data = data)
    if serializer.is_valid():
        follower_id = data['follower_id']
        followed_id = data['followed_id']
        if follower_id == followed_id:
            return responseGenerator('Invalid Input' , 406)
        if not is_id_in_accounts(follower_id):
            return responseGenerator('Invalid Follower' , 406)
        elif not is_id_in_accounts(followed_id):
            return responseGenerator('Invalid Follwed' , 406)
        else:
            return serializer
    else:
        return responseGenerator('Invalid Input', 406)


def is_id_in_accounts(id):
    try:
        account = AccountBasic.objects.get(pk = id)
        return True
    except AccountBasic.DoesNotExist:
        return False


def responseGenerator(msg , statusType):
    statusT = status.HTTP_200_OK
    if statusType == 406:
        statusT = status.HTTP_406_NOT_ACCEPTABLE
    return Response({'msg':msg}, statusT)