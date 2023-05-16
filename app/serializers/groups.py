from rest_framework import serializers

from app.models import *


class GroupsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')
