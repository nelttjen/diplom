from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound

from app.modules import query_debugger
from app.models import *
from diplom.serializers.default import DefaultSerializer
from app.serializers.group_lessons import GroupsListSerializer, GroupLessonsSerializer


class GroupLessonsView(APIView):

    # @query_debugger
    def get(self, request):
        group = request.GET.get('group', None)
        if not group or not (group := Group.objects.filter(id=group, is_active=True).first()):
            raise NotFound('group not found')
        lessons = Lesson.objects.filter(group=group, is_active=True).all()
        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GroupLessonsSerializer(lessons, many=True).data,
            'extra': {'group_name': group.name}
        }).data)


class GroupListView(APIView):

    def get(self, request):
        exclude = request.GET.get('exclude', None)
        groups = Group.objects.exclude(id__in=list(map(int, exclude.split(',')))).all()
        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GroupsListSerializer(groups, many=True).data
        }).data)