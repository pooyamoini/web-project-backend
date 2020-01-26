from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import AccountBasic
from .serializers import AccountSerializer


@csrf_exempt
def get_accounts(request):
    """
    List all accounts
    """
    accounts = AccountBasic.objects.all()
    account_serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(account_serializer.data, safe=False)


@csrf_exempt
@api_view(['GET', 'POST'])
def sample_test(request):
    if request.method == 'GET':
        return HttpResponse('hello')
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer, end="\n\n\n\n\n\n")
        return HttpResponse('hi')
    return HttpResponse('bye')
