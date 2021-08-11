from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from projects.models import Project
from projects.serializers import (ProjectAssignSerializer,
                                  ProjectCreateSerializer)
from users.permissions import IsAccountOwner


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permissions_classes = [IsAuthenticated, IsAccountOwner]

    def get_queryset(self):
        """
        This view should return a list of all projects where current user
        is an owner or a collaborator
        """
        user = self.request.user
        if user.is_anonymous:
            return Project.objects.none()
        return Project.objects.filter(Q(owner=user) | Q(coworkers__in=[user]))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        project.owner = request.user
        project.save(update_fields=['owner'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(detail=True, methods=['PATCH'])
    def assign(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectAssignSerializer(project,
                                             data=request.data,
                                             partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response('Project successfully assigned',
                        status=status.HTTP_200_OK,
                        headers=headers)
