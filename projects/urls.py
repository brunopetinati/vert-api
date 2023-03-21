from django.urls import path

from .views import ProjectGetByIdAPIView, ProjectListCreate, ProjectUpdateAPIView, ProjectDeleteAPIView

urlpatterns = [
    path("projects/", ProjectListCreate.as_view(), name="project-list"),
    path("projects/<int:id>/", ProjectGetByIdAPIView.as_view(), name="project-detail"),
    path("projects/<int:id>/update/", ProjectUpdateAPIView.as_view(), name="project-update"),
    path("projects/<int:id>/delete/", ProjectDeleteAPIView.as_view(), name="project-delete"),
]
