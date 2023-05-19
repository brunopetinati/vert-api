from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
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


class ProjectByDateAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        date = self.request.query_params.get("date", None)
        if date:
            return self.queryset.filter(created_at__gte=date)
        else:
            return self.queryset


class ProjectByDateRangeAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)
        if start_date and end_date:
            return self.queryset.filter(
                Q(created_at__lte=end_date) & Q(updated_at__gte=start_date)
            )
        else:
            return self.queryset.none()


class ProjectBeforeDateAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        try:
            date_str = self.request.query_params.get("date", None)
            if not date_str:
                raise ValidationError("Date parameter is required.")

            date = make_aware(datetime.strptime(date_str, "%Y-%m-%d"))

        except (ValueError, ValidationError) as e:
            raise ValidationError(str(e))

        return Project.objects.filter(created_at__lt=date)


def verify_password(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    password = request.data.get("password")

    if check_password(password, project.password):
        return download_file(request, project_id, field_name)
    else:
        return Response(
            {"error": "Senha inválida."}, status=status.HTTP_401_UNAUTHORIZED
        )
