from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project
from users.serializers import UserSerializer


class ProjectCreateSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'created_date']
        read_only_fields = ['id', 'owner', 'created_date']


class ProjectAssignSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    coworkers = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=get_user_model().objects.filter(is_active=True))

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'coworkers']
        read_only_fields = ['id', 'name', 'owner']

    def update(self, instance, validated_data):
        print(f'validated_data: {validated_data}')
        coworkers = validated_data.pop('coworkers', None)
        for coworker in coworkers:
            if coworker.id == instance.owner.id:
                raise serializers.ValidationError(
                    "You cannot collaborate with yourself.")
            instance.coworkers.add(coworker)
        instance.save()
        return instance
