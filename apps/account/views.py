from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import AccountBasic, LoggInBasic
from .serializers import AccountSerializer, LogginSerializer
from ..account_generic.models import AccountGeneric
from ..account_generic.serializers import AccountGenericSerializer
from django.core.mail import send_mail
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
                ag = AccountGeneric(
                    account=AccountBasic.objects.get(pk=data['username']))
                ag.save()
                return Response({'msg': 'You are successfully registered'}, status.HTTP_200_OK)
            else:
                return Response({'msg': 'something wrong :('}, status.HTTP_406_NOT_ACCEPTABLE)
    content = {'msg': 'Not valid Data'}
    return(Response(content, status.HTTP_406_NOT_ACCEPTABLE))


@csrf_exempt
@api_view(['PUT'])
def edit(request):
    data = request.data
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


@csrf_exempt
@api_view(['POST'])
def generate_suggestions(request):
    data = request.data
    if len(data.keys() & {'token'}) >= 1:
        token = request.data['token']
        try:
            my_account = LoggInBasic.objects.get(token=token).account
            suggestions = []
            for ac in range(min(10, len(AccountGeneric.objects.all()))):
                acc = AccountBasic.objects.all()[ac]
                if acc.username == my_account.username:
                    continue
                genacc = AccountGeneric.objects.get(account=acc)
                if genacc.followers.filter(username=my_account.username).exists():
                    continue
                suggestions.append(acc)
            data = AccountSerializer(suggestions, many=True)
            return Response({'msg': data.data}, status.HTTP_200_OK)
        except LoggInBasic.DoesNotExist:
            return Response({'msg': 'invalid token'}, status.HTTP_406_NOT_ACCEPTABLE)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid username'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)

@csrf_exempt
@api_view(['POST'])
def forget_password(request):
    data = request.data
    if len(data.keys() & {'email'}) >= 1:
        try:
            account = AccountBasic.objects.get(email=data['email'])
            new_password = random.randrange(111111, 999999)
            account.password = str(new_password)
            account.save()
            send_mail('Reset Password',
            'Your Password : ' + str(new_password),
            'webproject.fall.2019@gmail.com',
            [data['email']],
            fail_silently=False
            )
            return Response({'msg': 'succesfull'}, status.HTTP_200_OK)
        except AccountBasic.DoesNotExist:
            return Response({'msg': 'invalid email'}, status.HTTP_406_NOT_ACCEPTABLE)
    return Response({'msg': 'invalid data'}, status.HTTP_406_NOT_ACCEPTABLE)
