from django.contrib import admin
from models import Task, Occurrence, TaskType
from forms import OccurrenceForm


class OccurrenceInline(admin.StackedInline):
    model = Occurrence
    extra = 1
    form = OccurrenceForm


class TaskAdmin(admin.ModelAdmin):
    inlines = [OccurrenceInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = '__unicode__', 'project', 'programme', 'account', 'status'

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskType)
