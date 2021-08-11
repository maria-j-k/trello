from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from projects.models import Issue, Project
from projects.serializers import (IssueSerializer,
                                  ProjectAssignSerializer,
                                  ProjectCreateSerializer)
from projects.permissions import (IsOwner, IsAssignedToProject,
                                  IsAssignedToIssue)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]

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


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions.
        """
        if self.action == 'list':
            permission_classes = [IsAssignedToProject]
        elif self.action == 'partial_update':
            permission_classes = [IsAssignedToIssue]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        This view should return a list of all issues within a given task.
        """
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        return Issue.objects.filter(project=project)

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue = serializer.save()
        issue.project = project
        issue.owner = project.owner
        issue.save(update_fields=['owner', 'project'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(detail=True, methods=['PATCH'])
    def assign(self, request, project_pk, pk):
        issue = get_object_or_404(Issue, pk=pk)
        serializer = IssueSerializer(issue,
                                     data=request.data,
                                     partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response('Issue successfully assigned',
                        status=status.HTTP_200_OK,
                        headers=headers)
    # list - Is assinged to project or issue
    # create is owner
    # assign is owner
    # update is owner or is assigned to issue
    # delete is owner
