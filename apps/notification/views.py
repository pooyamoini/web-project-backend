from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from ..account.models import AccountBasic
from ..account.serializers import AccountSerializer
from ..post.models import Post
from ..post.serializers import PostSerializer
import string
import random
import datetime
import math


@csrf_exempt
@api_view(['POST'])
def index(request):
    pass
