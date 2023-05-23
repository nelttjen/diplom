from django.shortcuts import render

from app.models import Group


def index(request):
    groups = Group.objects.filter(is_active=True).only('id', 'name')
    return render(request, 'app/index.html', {'groups': groups})

