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
from .models import AccountGeneric
from .serializers import AccountGenericSerializer
from ..account.models import LoggInBasic, AccountBasic


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
            data = {'name': account.name,
                    'username': username, 'bio': account.bio, 'nfollowers': account_generic.followers.count(), 'nfollowings': account_generic.followings.count(), 'npost': account_generic.posts.count(), 'profile': account.profile, }
            return Response({'msg': data}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid username'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)
