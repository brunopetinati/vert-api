from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from accounts.models import CustomUser

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectGetByIdAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "id"  # Campo usado para buscar o objeto no banco de dados


class ProjectUpdateAPIView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "id"


class ProjectDeleteAPIView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "id"


def download_file(request, project_id, field_name):
    project = get_object_or_404(Project, id=project_id)
    file_field = getattr(project, field_name)
    if not file_field:
        return HttpResponse("Arquivo não encontrado", status=404)
    file_content = file_field.read()
    response = HttpResponse(file_content, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
        file_field.name
    )
    return response


class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid user ID"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.id != user.id:
            return Response(
                {"error": "You do not have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )

        projects = Project.objects.filter(owner=user)
        serializer = self.serializer_class(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
