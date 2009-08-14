from hostel.decorators import rendered
from models import Project

@rendered
def project_list(request):
    return 'policy/project_list.html', {
        'object_list': Project.objects.all(),
    }

