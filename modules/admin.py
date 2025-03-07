from django.contrib import admin
from .models import Module, Permission

# Register your models here.
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at', 'module')
    list_filter = ('name', 'created_at', 'updated_at', 'module')
    search_fields = ('name', 'description')
    ordering = ('name',)

admin.site.register(Module, ModuleAdmin)
admin.site.register(Permission, PermissionAdmin)
