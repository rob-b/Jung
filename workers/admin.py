from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import Employee, Skill

class EmployeeAdmin(admin.StackedInline):
    model = Employee
    fk_name = 'user'
    # max_num = 1
    verbose_name = 'profile'
    verbose_name_plural = 'Profile'
    filter_horizontal = 'skill',

class EmployeeUserAdmin(UserAdmin):
    inlines = [EmployeeAdmin]

admin.site.unregister(User)
admin.site.register(User, EmployeeUserAdmin)
admin.site.register(Skill)
