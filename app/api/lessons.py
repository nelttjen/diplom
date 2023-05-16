import json

from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from pydantic import ValidationError

from app.models import *
from app.serializers.lessons import GroupLessonsSerializer
from app.typing import SettingsRequest
from app.modules import LessonsGenerator
from diplom.serializers.default import DefaultSerializer


class GroupLessonsView(APIView):

    def get(self, request):
        group = request.GET.get('group', None)
        if not group or not (group := Group.objects.filter(id=group, is_active=True).prefetch_related(
            Prefetch('lessons', Lesson.objects.filter(is_active=True).select_related('teacher', 'cabinet'))
        ).first()):
            raise NotFound('group not found')

        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': GroupLessonsSerializer(group.lessons, many=True).data,
            'extra': {'group_name': group.name}
        }).data)

    def post(self, request):

        settings = json.loads(request.data.get('groups', '{}'))

        try:
            req_settings = SettingsRequest.parse_obj({'groups': settings})
        except ValidationError as e:
            raise ParseError(f"Wrong settings in request: {e.json()}")

        # try:
        generator = LessonsGenerator(settings=req_settings)
        generator.generate()
        # except Exception as e:
        #     raise ParseError(f"Невозможно сгенерировать рассписание для выбранного {e}")

        return Response(DefaultSerializer({
            'msg': 'ok',
            'content': generator.generated.to_representation(lessons=generator.lessons, groups=generator.groups)
        }).data)