from django.contrib import admin

from projects.models import Project, Task, TaskTimeTrack

# Register your models here.
admin.register(Project)
admin.register(Task)
admin.register(TaskTimeTrack)
