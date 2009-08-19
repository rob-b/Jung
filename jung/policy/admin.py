from django.contrib import admin
from models import Account, Programme, Project

class PolicyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Account, PolicyAdmin)
admin.site.register(Programme, PolicyAdmin)
admin.site.register(Project, PolicyAdmin)
