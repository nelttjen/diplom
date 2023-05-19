from rest_framework import serializers

from app.models import GeneratedLessons


class GeneratedScheduleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneratedLessons
        fields = ('id', 'name', 'created_at')


class GeneratedScheduleInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneratedLessons
        fields = '__all__'
