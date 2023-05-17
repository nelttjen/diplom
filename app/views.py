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


def shedules(request):
    response = requests.get('http://127.0.0.1:8000/api/schedules/').json()
    items = [GeneratedLessons(**item) for item in response['content']]
    return render(request, 'app/schedules.html', {'items': items})


def show_schedule(request, schedule_id):
    response = requests.get(f'http://127.0.0.1:8000/api/schedules/{schedule_id}/')
    if response.status_code != 200:
        return HttpResponseNotFound()
    return render(request, 'app/show_schedule.html', {'item': GeneratedLessons(**response.json()['content'])})