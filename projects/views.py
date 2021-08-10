from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import (ProjectAssignSerializer,
                                  ProjectCreateSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    @action(detail=True, methods=['PATCH'])
    def assign(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectAssignSerializer(project,
                                             data=request.data,
                                             partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response('Project successfully assigned',
                        status=status.HTTP_200_OK,
                        headers=headers)
