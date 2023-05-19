from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import permissions

from diplom.serializers.default import DefaultSerializer
from app.models import GeneratedLessons
from app.serializers.lesson_schedule import GeneratedScheduleListSerializer, GeneratedScheduleInfoSerializer


class ScheduleListView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        count = int(request.GET.get('count', 20))
        page = int(request.GET.get('page', 1))

        items = GeneratedLessons.objects.order_by('-created_at').all()[count*(page-1):count*page]

        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GeneratedScheduleListSerializer(items, many=True).data
        }).data)


class ScheduleView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, schedule_id):
        try:
            schedule = GeneratedLessons.objects.get(pk=schedule_id)
        except GeneratedLessons.DoesNotExist:
            raise NotFound('schedule not found')

        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GeneratedScheduleInfoSerializer(schedule).data
        }).data)
