import requests

from django.db.models import Prefetch
from django.shortcuts import render
from django.http import HttpResponseNotFound

from app.models import *
from app.modules import query_debugger


# Create your views here.
@query_debugger
def index(request):
    groups = Group.objects.filter(is_active=True).only('id', 'name')
    return render(request, 'app/index.html', {'groups': groups})

