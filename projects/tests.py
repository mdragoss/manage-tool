from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from users.models import User
from projects.models import Project, Task
from projects.views import ProjectViewSet


# Create your tests here.
class TestProjects(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='user@mail.com',
            password='password',
            first_name='First',
            last_name='Last',
        )
        self.project = Project(
            project_name='Test project',
            description='Test description',
            phase='INITIATION',
            created_by=self.user
        )
        self.project.save()
        self.task = Task(
            task_name='Task name',
            task_status='OPEN',
            description='Task description',
            created_at='2024-01-01T18:55:09.455Z',
            project=self.project,
        )
        self.task.save()

    def test_get_projects(self):
        request = self.factory.get(
            path='api/projects/',
            format='json',
        )
        force_authenticate(request=request, user=self.user)
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_projects_unauthorized(self):
        request = self.factory.get(
            path='api/projects/',
            format='json',
        )
        view = ProjectViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
