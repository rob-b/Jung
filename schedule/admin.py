from django.contrib import admin
from models import Task, Occurrence, TaskType


class OccurrenceInline(admin.StackedInline):
    model = Occurrence
    extra = 1


class TaskAdmin(admin.ModelAdmin):
    inlines = [OccurrenceInline]

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskType)
