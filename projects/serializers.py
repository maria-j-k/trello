from rest_framework import serializers
from projects.models import Project


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'owner', 'name']
        read_only_fields = ['id', 'owner']


class ProjectAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'owner']
        read_only_fields = ['id', 'name']

    def update(self, instance, validated_data):
        owner = validated_data.pop('owner', None)
        instance.owner_id = owner
        instance.save(update_fields=['owner'])
        return instance
