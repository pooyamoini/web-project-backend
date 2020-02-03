from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
def index(request):
    send_mail('Hello Kiri',
    'Hey How you doing?',
    'alireza.am1379@gmail.com',
    ['pooyamoini2000@gmail.com'],
    fail_silently=False
    )
    return render(request, 'send/index.html')