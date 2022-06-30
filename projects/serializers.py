from datetime import date
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from projects.models import Issue, Project


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
        coworkers = validated_data.pop('coworkers', None)
        for coworker in coworkers:
            if coworker.id == instance.owner.id:
                raise serializers.ValidationError(
                    "You cannot collaborate with yourself.")
            instance.coworkers.add(coworker)
        instance.save()
        return instance


class IssueSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(
            required=False,
            queryset=get_user_model().objects.filter(is_active=True))

    class Meta:
        model = Issue
        fields = ['id', 'project', 'owner', 'title', 'description',
                  'due_date', 'assignee', 'status']
        read_only_fields = ['id']

    def validate_due_date(self, value):
        """
        Ensures that the due date is not in the past
        """
        if value <= timezone.now().date():
            raise serializers.ValidationError("Due date cannot be past date.")
        return value
