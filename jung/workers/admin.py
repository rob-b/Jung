from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import Skill, Role, Employee
from contacts.models import InstantMessenger


class InstantMessengerAdmin(admin.StackedInline):
    model = InstantMessenger


class EmployeeAdmin(admin.StackedInline):
    model = Employee
    fk_name = 'user'
    max_num = 1
    verbose_name = 'profile'
    verbose_name_plural = 'Profile'
    filter_horizontal = 'skill',
    inlines = [InstantMessengerAdmin]


class EmployeeUserAdmin(UserAdmin):
    inlines = [EmployeeAdmin]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Groups'), {'fields': ('groups',), 'classes': ('collapse',)}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_active', 'is_superuser',
                       'user_permissions'),
            'classes': ('collapse',),
        }),
    )


class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class SkillAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.unregister(User)
admin.site.register(User, EmployeeUserAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(InstantMessenger)
