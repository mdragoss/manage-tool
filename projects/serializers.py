from attr import field, fields
from rest_framework import serializers

from projects.models import Project, Task, TaskTimeTrack
from users.serializers import UserSerializer


class ProjectSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('created_at', 'modified_at', 'created_by')


class ProjectReturnSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('id', 'created_by')


# class ProjectTaskSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Task
#         exclude = ('user', 'project')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('user', 'project')


class TaskRetrieveUpdateSerializer(serializers.ModelSerializer):
    project = ProjectSerilizer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskTimeTrackSerializer(serializers.ModelSerializer):
    task = TaskListSerializer(read_only=True)

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        time_tracked = (
            TaskTimeTrack.objects.filter(task_id=self.context['task'])
            .order_by('-end_time')
            .first()
        )

        if time_tracked:
            if start_time < time_tracked.end_time:
                raise serializers.ValidationError(
                    {'detail': 'Start time should be greater than last logged time.'}
                )

        if start_time > end_time:
            raise serializers.ValidationError(
                {'detail': 'Start time should not be greater than end time.'}
            )

        if start_time == end_time:
            raise serializers.ValidationError(
                {'detail': 'End time should be different from start.'}
            )
        
        # many other validation could be
        return attrs

    class Meta:
        model = TaskTimeTrack
        fields = '__all__'
