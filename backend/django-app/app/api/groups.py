from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Group
from diplom.serializers.default import DefaultSerializer
from app.serializers.groups import GroupsListSerializer


class GroupListView(APIView):

    def get(self, request):
        exclude = request.GET.get('exclude', None)
        groups = Group.objects.filter(is_active=True)
        if exclude is not None:
            groups = groups.exclude(id__in=list(map(int, exclude.split(','))))
        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GroupsListSerializer(groups, many=True).data
        }).data)
