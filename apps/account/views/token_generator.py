from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from ..models import AccountBasic, LoggInBasic
from ..serializers import AccountSerializer, LogginSerializer
import string
import random
import datetime


@csrf_exempt
@api_view(['POST'])
def login(request):
    data = request.data
    if len(data.keys() & {'username', 'password'}) >= 2:
        try:
            account = AccountBasic.objects.get(pk=data['username'])
            if account.password == data["password"]:
                token = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(100))
                logged_in_account = LoggInBasic(
                    account=account, token=token, token_gen_time=datetime.datetime.now())
                logged_in_account.save()
                return Response({'msg': 'successfull', 'token': token}, status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid username/password. \t please try again'}, status.HTTP_406_NOT_ACCEPTABLE)

        except AccountBasic.DoesNotExist:
            return Response({'msg': 'username does not exist'}, status.HTTP_406_NOT_ACCEPTABLE)

    content = {'msg': 'Not valid Data'}
    return(Response(content, status.HTTP_406_NOT_ACCEPTABLE))


@csrf_exempt
@api_view(['POST'])
def token_isvalid(request):
    data = request.data
    if len(data.keys() & {'token'}) >= 1:
        try:
            token = data["token"]
            query_res = LoggInBasic.objects.get(token=token)
            if (datetime.datetime.now(datetime.timezone.utc) - query_res.token_gen_time).seconds >= 3600 * 3:
                return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
            account = query_res.account
            account_serializer = AccountSerializer(account)
            return Response({'msg': 'valid token', 'account': account_serializer.data}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)

    content = {'msg': 'Not valid Data'}
    return(Response(content, status.HTTP_406_NOT_ACCEPTABLE))
