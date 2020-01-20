# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

def index(reguest):
    return HttpResponse("You enter to account")
