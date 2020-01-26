from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Account
from .serializers import AccountSerializer

@csrf_exempt
def get_accounts(request):
    """
    List all accounts
    """
    accounts = Account.objects.all()
    account_serializer = AccountSerializer(accounts, many=True)
    return JsonResponse(account_serializer.data, safe=False)

