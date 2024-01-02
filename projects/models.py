from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import User


class Project(models.Model):
    class ProjectPhase(models.TextChoices):
        INITIATION = 'INITIATION', _('Concept Phase')
        PLANNING = 'PLANNING', _('Definition Phase')
        EXECUTION = 'EXECUTION', _('Execution Phase')
        CONTROL = 'CONTROL', _('Control Phase')
        CLOSED = 'CLOSED', _('Closed Phase')

    project_name = models.CharField(max_length=100)
    description = models.TextField()
    phase = models.CharField(
        max_length=10,
        choices=ProjectPhase.choices,
        default=ProjectPhase.INITIATION,
    )
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)
    # customer = models.ForeignKey()
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        OPEN = 'OPEN', _('Task is open')
        IN_PROGRESS = 'IN_PROGRESS', _('Task is in progress')
        DONE = 'DONE', _('Task is done')
        BLOCKED = 'BLOCKED', _('Task is blocked by other')
        CANCELLED = 'CANCELLED', _('Task is canceled')

    task_name = models.CharField(max_length=100)
    task_status = models.CharField(
        max_length=11, choices=TaskStatus.choices, default=TaskStatus.OPEN
    )
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    story_points = models.IntegerField(null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    # pair_user = models.ForeignKey(
    #     to=User, null=True, on_delete=models.SET_NULL
    # )

    class Meta:
        db_table = 'task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskTimeTrack(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'task_time'
        verbose_name = 'TaskTime'
        verbose_name_plural = 'TasksTime'


# Message Model
# class Message(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="user"
#     )
#     sender = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="sender"
#     )
#     receiver = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="receiver"
#     )

#     message = models.CharField(max_length=10000)

#     is_read = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['date']
#         verbose_name_plural = "Message"

#     def __str__(self):
#         return f"{self.sender} - {self.receiver}"

#     @property
#     def sender_profile(self):
#         sender_profile = User.objects.get(user=self.sender)
#         return sender_profile

#     @property
#     def receiver_profile(self):
#         receiver_profile = User.objects.get(user=self.receiver)
#         return receiver_profile
