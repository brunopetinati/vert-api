from django.urls import path

from .views import (
    ProjectDeleteAPIView,
    ProjectGetByIdAPIView,
    ProjectListCreate,
    ProjectUpdateAPIView,
    UserProjectsView,
    download_file,
)

urlpatterns = [
    path("projects/", ProjectListCreate.as_view(), name="project-list"),
    path("projects/<int:id>/", ProjectGetByIdAPIView.as_view(), name="project-detail"),
    path(
        "projects/<int:id>/update/",
        ProjectUpdateAPIView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:id>/delete/",
        ProjectDeleteAPIView.as_view(),
        name="project-delete",
    ),
    path(
        "project/<int:project_id>/download/<str:field_name>/",
        download_file,
        name="download_file",
    ),
    path(
        "projects/<int:user_id>/by_user/",
        UserProjectsView.as_view(),
        name="project-list-by-user",
    ),
]
