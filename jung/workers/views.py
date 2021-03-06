from django.shortcuts import get_object_or_404
from hostel.decorators import rendered
from models import Employee, Skill

@rendered
def skill_detail(request, skill):
    skill = get_object_or_404(Skill, slug=skill)
    return 'workers/skill_detail.html', {
        'object': skill,
    }

@rendered
def skill_list(request):
    skills = Skill.objects.all()
    return 'workers/skill_list.html', {
        'object_list': skills,
    }
