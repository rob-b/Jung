from django.db import models


class SkillManager(models.Manager):
    """Manager that appends the count of employees that have this skill to the
    default queryset"""

    def get_query_set(self):
        qs = super(SkillManager, self).get_query_set()
        return qs.annotate(total_employees=models.Count('employee'))
