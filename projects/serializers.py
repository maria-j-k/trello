from django.contrib.auth import get_user_model
from rest_framework import serializers
from projects.models import Project


class ProjectCreateSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'coworker']
        read_only_fields = ['id', 'owner', 'coworker']


class ProjectAssignSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    coworker = serializers.PrimaryKeyRelatedField(
            queryset=get_user_model().objects.all())

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'coworker']
        read_only_fields = ['id', 'name', 'owner']

    def validate_coworker(self, value):
        """
        Check if the coworker has an active account.
        """
        if not value.is_active:
            raise serializers.ValidationError("This account is not active yet")
        return value

    def update(self, instance, validated_data):
        coworker = validated_data.pop('coworker', None)
        if coworker.id == instance.owner.id:
            raise serializers.ValidationError(
                    "You cannot collaborate with yourself.")
        instance.coworker = coworker
        instance.save(update_fields=['coworker'])
        return instance
