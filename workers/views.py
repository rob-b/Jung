from hostel.decorators import rendered
from models import Employee

@rendered
def employee_list(request):
    context = {
        'object_list': Employee.objects.select_related(),
    }
    return 'workers/employee_list.html', context
