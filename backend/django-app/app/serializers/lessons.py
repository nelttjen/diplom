from rest_framework import serializers

from app.models import Teacher, Lesson


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')


class GroupLessonsSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'teacher')
