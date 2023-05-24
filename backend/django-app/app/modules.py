import functools
import json
import random
import time
from typing import Dict

from django.db import connection, reset_queries

from diplom.settings import DEBUG
from app.typing import SettingsRequest, GenerateList
from app.models import GeneratedLessons, Group, Lesson


class LessonsGenerator:
    def __init__(self, settings: SettingsRequest, name: str):
        self.settings = settings

        self.generated = GenerateList()

        self.random_pair_choices = (
            (1, 2, 3, 4),
            (2, 3, 4, 1),
            (3, 4, 1, 2),
        )

        self.days = (
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'
        )

        self.groups = []
        self.lessons = []

        self.name = name

    def _dict_from_queryset(self, queryset):
        ret = {}

        for model in queryset:
            ret[model.id] = model
        return ret

    def get_groups(self, group_ids) -> Dict[int, 'Group']:
        return self._dict_from_queryset(Group.objects.filter(id__in=group_ids))

    def get_lessons(self, lesson_ids) -> Dict[int, 'Lesson']:
        return self._dict_from_queryset(Lesson.objects.filter(id__in=lesson_ids).select_related('teacher', 'cabinet'))

    def split_lessons(self, gr_id):
        for lesson in self.settings.groups[gr_id]:
            if lesson.count > 2:
                new_lesson = lesson.copy()
                new_lesson.count -= 2
                self.settings.groups[gr_id].append(new_lesson)
                lesson.count = 2

    def process_lesson(self, group, lesson, setup=None):

        gr_lesson = self.lessons[lesson.id]

        cabinet = gr_lesson.cabinet_id
        teacher = gr_lesson.teacher_id

        random_days = list(self.days)
        random.shuffle(random_days)

        if not isinstance(setup, list):
            setup = list(random.choice(self.random_pair_choices))

        while random_days:
            this_setup = setup.copy()
            day = random_days.pop(0)

            if lesson.count == 0:
                break

            while this_setup:
                index = this_setup.pop(0)

                if lesson.count == 0:
                    continue

                if not self.generated.is_available(day=day, index=index, cabinet=cabinet, teacher=teacher,
                                                   group=group.id):
                    print(f'not available: {day} {index} {group}')
                    continue
                if len(getattr(self.generated, day)[group.id]) >= group.max_day:
                    print(f'max this day: {day}')
                    continue

                self.generated.set_lesson_for_group(day=day, index=index,
                                                    cabinet=cabinet, teacher=teacher,
                                                    group=group.id, lesson=lesson.id)
                lesson.count -= 1

    def generate(self):
        group_ids = list(self.settings.groups.keys())
        lesson_ids = []
        for key in group_ids:
            lesson_ids.extend([lesson.id for lesson in self.settings.groups[key]])

        self.groups, self.lessons = self.get_groups(group_ids), self.get_lessons(lesson_ids)

        random.shuffle(group_ids)

        while group_ids:
            gr_id = group_ids.pop()
            group = self.groups[gr_id]

            self.generated.add_group(gr_id)
            self.split_lessons(gr_id)

            group_lesson_list = sorted(self.settings.groups[gr_id], key=lambda x: (x.count, x.lesson_name), reverse=True)

            for lesson in group_lesson_list:
                self.process_lesson(group, lesson)
                if lesson.count:
                    print(f'starting additional checks for {lesson} {gr_id}, before: {lesson.count}')
                    self.process_lesson(group, lesson, setup=[5, 6])
                    print(f'after cheks: {lesson.count}')
                    if lesson.count:
                        ret_dict = self.generated.to_representation(groups=self.groups, lessons=self.lessons)
                        GeneratedLessons.objects.create(
                            name="failed",
                            weekdays=ret_dict
                        )
                        raise Exception(f'{self.lessons[lesson.id].name}: cabinet or teacher reached limit')

        ret_dict = self.generated.to_representation(groups=self.groups, lessons=self.lessons)
        GeneratedLessons.objects.create(
            name=self.name,
            weekdays=ret_dict
        )
        return ret_dict


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        if DEBUG:
            print(f"View (function name): {func.__name__}")
            print(f"Queries quantity: {end_queries - start_queries}")
            print(f"Execution time: {(end - start):.2f}s")

        return result

    return inner_func