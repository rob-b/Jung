from django.shortcuts import get_object_or_404
from hostel.decorators import rendered
from models import Project

@rendered
def project_list(request):
    return 'policy/project_list.html', {
        'object_list': Project.objects.all(),
    }

@rendered
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return 'policy/project_detail.html', {
        'project': project,
    }

