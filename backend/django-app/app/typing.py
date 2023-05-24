from __future__ import annotations

import pydantic

from typing import List, Dict


class SettingsGroup(pydantic.BaseModel):
    id: int = pydantic.Field(default=..., alias='lesson_id')
    count: int = pydantic.Field(default=..., alias='count')

    class Config(pydantic.BaseConfig):
        extra = 'allow'


class SettingsRequest(pydantic.BaseModel):
    groups: Dict[int, List['SettingsGroup']]


class GenerateLesson(pydantic.BaseModel):
    id: int
    teacher: int
    cabinet: int
    index: int


class StatisticForTeacherDays(pydantic.BaseModel):
    monday: Dict[int, int]
    tuesday: Dict[int, int]
    wednesday: Dict[int, int]
    thursday: Dict[int, int]
    friday: Dict[int, int]
    saturday: Dict[int, int]

    @classmethod
    def default(cls):
        return cls.parse_obj({
            'monday': {},
            'tuesday': {},
            'wednesday': {},
            'thursday': {},
            'friday': {},
            'saturday': {},
        })


class GenerateList(pydantic.BaseModel):
    monday: Dict[int, List['GenerateLesson']] = pydantic.Field(default={})
    tuesday: Dict[int, List['GenerateLesson']] = pydantic.Field(default={})
    wednesday: Dict[int, List['GenerateLesson']] = pydantic.Field(default={})
    thursday: Dict[int, List['GenerateLesson']] = pydantic.Field(default={})
    friday: Dict[int, List['GenerateLesson']] = pydantic.Field(default={})
    saturday: Dict[int, List['GenerateLesson']] = pydantic.Field(default={})

    statistic: 'StatisticForTeacherDays' = pydantic.Field(default=StatisticForTeacherDays.default())

    def get_count_teacher_for_day(self, day, teacher_id):

        daily_dict: Dict[int, int] = getattr(self.statistic, day)

        count = daily_dict.get(teacher_id, None)
        if count is None:
            daily_dict[teacher_id] = 0
            count = 0
        return count

    def teacher_check_lessons_for_day(self, day, teacher_id, max_lessons_for_day):
        return max_lessons_for_day > self.get_count_teacher_for_day(day, teacher_id)

    def is_cabinet_available(self, day, cabinet_id, index):
        day_dict: Dict[int, List['GenerateLesson']] = getattr(self, day)

        for group_lessons in day_dict.values():
            for lesson in group_lessons:
                lesson: 'GenerateLesson'
                if lesson.index == index and lesson.cabinet == cabinet_id:
                    return False
        return True

    def is_teacher_available(self, day, teacher_id, index):
        day_dict: Dict[int, List['GenerateLesson']] = getattr(self, day)

        for group_lessons in day_dict.values():
            for lesson in group_lessons:
                lesson: 'GenerateLesson'
                if lesson.index == index and lesson.teacher == teacher_id:
                    return False
        return True

    def is_index_available(self, day, index, group):
        day_dict: Dict[int, List['GenerateLesson']] = getattr(self, day)

        for lesson in day_dict[group]:
            lesson: 'GenerateLesson'
            if lesson.index == index:
                return False
        return True

    def fields(self):
        return [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday]

    def add_group(self, gr_id):
        for field in self.fields():
            field[gr_id] = []

    def is_available(self, day, index, cabinet, teacher, group):
        av_cab = self.is_cabinet_available(day=day, cabinet_id=cabinet, index=index)
        av_teacher = self.is_teacher_available(day=day, teacher_id=teacher, index=index)
        av_index = self.is_index_available(day=day, index=index, group=group)

        available = av_cab and av_teacher and av_index

        print(av_cab, av_teacher, av_index, day, group, index)

        return available

    def set_lesson_for_group(self, day, index, group, lesson, cabinet, teacher):
        field = getattr(self, day)

        field[group].append(GenerateLesson.parse_obj({
            'id': lesson, 'teacher': teacher, 'cabinet': cabinet, 'index': index
        }))
        field[group] = sorted(field[group], key=lambda x: x.index)

        try:
            getattr(self.statistic, day)[teacher] += 1
        except:
            getattr(self.statistic, day)[teacher] = 1

    def to_representation(self, groups, lessons):
        represent = self.dict()
        represent_copy = {}
        for field in represent.keys():
            val = []
            if field == 'statistic':
                val = {}
            represent_copy[field] = val

        teachers = set()

        for less in lessons.values():
            teachers.add(less.teacher)

        for key, val in represent.items():
            if key == 'statistic':
                continue
            for group_id, lessons_list in val.items():
                represent_lessons = []

                for lesson in lessons_list:
                    model = lessons[lesson['id']]
                    represent_lessons.append({
                        'lesson_name': model.name,
                        'lesson_teacher': f'{model.teacher.first_name} {model.teacher.last_name}',
                        'lesson_cabinet': model.cabinet.name,
                        'lesson_index': lesson['index']
                    })
                represent_copy[key].append({
                    'group_id': group_id,
                    'group_name': groups[group_id].name,
                    'lessons': represent_lessons
                })

        for key, val in represent['statistic'].items():
            day_teachers = []

            for teacher_id, teacher_count in val.items():
                teacher_name = ''

                for model in teachers:
                    if model.id == teacher_id:
                        teacher_name = f'{model.first_name} {model.last_name}'

                day_teachers.append(
                    {'teacher_name': teacher_name, 'count': teacher_count}
                )

            represent_copy['statistic'][key] = day_teachers

        return represent_copy
