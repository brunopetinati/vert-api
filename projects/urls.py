from django.urls import path
from .views import ProjectListCreate, ProjectGetByIdAPIView

urlpatterns = [
path('projects/', ProjectListCreate.as_view(), name='project-list'),
path('projects/<int:id>/', ProjectGetByIdAPIView.as_view(), name='project-detail'),
]