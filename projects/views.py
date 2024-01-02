from asyncio import Task

from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import UpdateAPIView, ListAPIView

from projects.models import Project, Task
from projects.serializers import (
    ProjectReturnSerializer,
    ProjectSerializer,
    TaskListSerializer,
    TaskRetrieveUpdateSerializer,
    TaskTimeTrackSerializer,
)


# Create your views here.
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    @extend_schema(
        responses={
            200: ProjectSerializer(many=True),
            401: OpenApiResponse(description='Unauthorized'),
        }
    )
    def list(self, request):
        projects = self.get_queryset()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            201: ProjectSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
        },
        request=ProjectSerializer,
    )
    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={
            201: ProjectSerializer,
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        }
    )
    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            201: ProjectReturnSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        },
        request=ProjectSerializer,
    )
    def update(self, request, pk=None):
        data = request.data
        data['modified_at'] = timezone.now()
        project = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ProjectSerializer(project, data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return_data = ProjectReturnSerializer(result)
        return Response(return_data.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            201: ProjectReturnSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        },
        request=ProjectSerializer,
    )
    def partial_update(self, request, pk=None):
        data = request.data
        data['modified_at'] = timezone.now()
        project = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return_data = ProjectReturnSerializer(result)
        return Response(return_data.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: OpenApiResponse(description='Success'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        },
        request=ProjectSerializer,
    )
    def destroy(self, request, pk=None):
        raise NotImplemented('Not implemented')

    @action(
        detail=False, methods=['post'], url_path='transfer-project-to-user'
    )
    def transfer_project_to_user(self, request, pk=None):
        pass

    @extend_schema(
        responses={
            201: TaskListSerializer,
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        },
        request=TaskListSerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH
            )
        ],
    )
    @action(
        detail=True,
        methods=['post'],
        url_path='create-task',
        url_name='create-task',
    )
    def create_project_task(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        task_serializer = TaskListSerializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.save(project=project)
        return Response(
            TaskListSerializer(task).data, status=status.HTTP_201_CREATED
        )

    @extend_schema(
        responses={
            200: TaskListSerializer,
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        },
        request=TaskListSerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH
            )
        ],
    )
    @action(
        detail=True,
        methods=['get'],
        url_path='project-tasks',
        url_name='project-tasks',
    )
    def get_project_tasks(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        tasks = Task.objects.filter(project=project)
        task_serializer = TaskListSerializer(tasks, many=True)
        return Response(task_serializer.data, status=status.HTTP_200_OK)


class TaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(UpdateAPIView):
    serializer_class = TaskRetrieveUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.all()


class TaskTimeTrack(ViewSet):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Success'),
            400: OpenApiResponse(description='Bad Request'),
            401: OpenApiResponse(description='Unauthorized'),
            404: OpenApiResponse(description='Not found'),
        },
        request=TaskTimeTrackSerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH
            )
        ],
    )
    @action(
        detail=True,
        methods=['post'],
        url_path='tasks-time',
    )
    def task_time_track(self, request, pk=None):
        task = get_object_or_404(Task.objects.filter(user=request.user), pk=pk)
        serializer = TaskTimeTrackSerializer(
            data=request.data, context={'task': task.id}
        )
        serializer.is_valid(raise_exception=True)
        result = serializer.save(task=task)

        return Response(
            TaskTimeTrackSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )
