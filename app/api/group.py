from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from diplom.serializers.default import DefaultSerializer
from app.serializers.groups import GroupsListSerializer


class GroupListView(APIView):

    def get(self, request):
        exclude = request.GET.get('exclude', None)
        groups = Group.objects.exclude(id__in=list(map(int, exclude.split(',')))).all()
        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GroupsListSerializer(groups, many=True).data
        }).data)
