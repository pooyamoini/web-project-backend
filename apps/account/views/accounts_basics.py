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
def get_accounts(request):
    """
    List all accounts
    """
    accounts = AccountBasic.objects.all()
    account_serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(account_serializer.data, safe=False)


@csrf_exempt
@api_view(['POST'])
def signup(request):
    data = request.data
    if len(data.keys() & {'email', 'name', 'username', 'password'}) == 4:
        try:
            account = AccountBasic.objects.get(pk=data['username'])
            return Response({'msg': 'This username already exist'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            serializer = AccountSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'You are successfully registered'}, status.HTTP_200_OK)
            else:
                return Response({'msg': 'something wrong :('}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return(Response(content, status.HTTP_406_NOT_ACCEPTABLE))


@csrf_exempt
@api_view(['PUT'])
def edit(request):
    data = request.data
    print('--'*70)
    print(data)
    print('--'*70)
    if len(data.keys() & {'email', 'name', 'username', 'password', 'token'}) >= 4:
        try:
            account = LoggInBasic.objects.get(token=data['token']).account
            for (key, value) in data.items():
                if (value == '' or value == None or key == 'username'):
                    continue
                try:
                    temp = getattr(account, key)
                    setattr(account, key, value)
                except AttributeError:
                    if key == 'newPassword':
                        if data['newPassword'] == data['confirmNewPassword']:
                            if data['password'] == account.password:
                                account.password = data['newPassword']
                                continue
                            return Response({'msg': 'wrong password'}, status.HTTP_406_NOT_ACCEPTABLE)
                        return Response({'msg': 'passwords doesnt match'}, status.HTTP_406_NOT_ACCEPTABLE)
                    continue
            account.save()
            return Response({'msg': 'successfull'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'username does not exist'}, status.HTTP_406_NOT_ACCEPTABLE)

    content = {'msg': 'Not valid Data'}
    return(Response(content, status.HTTP_406_NOT_ACCEPTABLE))


@csrf_exempt
@api_view(['DELETE'])
def del_profile(request):
    data = request.data
    if len(data.keys() & {'username', 'password'}) >= 2:
        try:
            account = AccountBasic.objects.get(pk=data['username'])
            account_serializer = AccountSerializer(account, data=data)
            if account_serializer.is_valid():
                if account.password == data["password"]:
                    account.delete()
                    return Response({'msg': 'successfull'}, status.HTTP_200_OK)
                else:
                    return Response({'msg': 'wrong password'}, status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'msg': 'something wrong'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'username does not exist'}, status.HTTP_406_NOT_ACCEPTABLE)

    content = {'msg': 'Not valid Data'}
    return(Response(content, status.HTTP_406_NOT_ACCEPTABLE))


@csrf_exempt
@api_view(['POST'])
def change_profile(request):
    data = request.data
    if len(data.keys() & {'token', 'profile'}) >= 2:
        try:
            token = data['token']
            profile_path = data['profile']
            account = LoggInBasic.objects.get(token=token).account
            account.profile = profile_path
            account.save()
            return Response({'msg': 'successfull'}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)
