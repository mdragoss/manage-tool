from django.urls import include, path
from rest_framework.routers import DefaultRouter

from projects.views import (
    ProjectViewSet,
    TaskListView,
    TaskUpdateView,
    TaskTimeTrack,
)

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename="projects")
router.register('tasks', TaskTimeTrack, basename="tasks-time")

project_routes = [
    path('', include(router.urls)),
    path('tasks/<int:pk>/', TaskUpdateView.as_view()),
    path('tasks/', TaskListView.as_view(), name='tasks'),
]
