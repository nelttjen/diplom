from rest_framework import serializers

from app.models import Group


class GroupsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')
