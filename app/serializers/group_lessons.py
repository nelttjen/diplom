from rest_framework import serializers

from app.models import *


class TeacherListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')


class GroupLessonsSerializer(serializers.ModelSerializer):
    teacher = TeacherListSerializer()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'require_comp', 'teacher')


class GroupsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')
