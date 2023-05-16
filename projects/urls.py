from django.urls import path

from .views import (
    ProjectDeleteAPIView,
    ProjectGetByIdAPIView,
    ProjectListCreate,
    ProjectUpdateAPIView,
    UserProjectsView,
    download_file,
    ProjectByDateAPIView,
    ProjectByDateRangeAPIView,
    ProjectBeforeDateAPIView,
    verify_password
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
    path(
        "projects/by_date/",  
        ProjectByDateAPIView.as_view(),
        name="project-list-by-date",
    ),
    path(
        "projects/by_date_range/",  
        ProjectByDateRangeAPIView.as_view(),
        name="project-list-by-date-range",
    ),
    path(
        "projects/before_date/", 
        ProjectBeforeDateAPIView.as_view(), 
        name="project-list-before-date"
    ),
    path(
        'project/<int:project_id>/verify_password/', 
        verify_password,
        name="verify_password"
    ),
]
