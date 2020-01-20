# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import json


def index(reguest):
    return HttpResponse(json.dumps({"name": "pooya"}))
