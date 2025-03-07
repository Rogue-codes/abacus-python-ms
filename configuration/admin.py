from django.contrib import admin
from configuration.models import Configuration

# Register your models here.
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('business', 'darkMode', 'MFA', 'staff_change_First_password', 'force_password_Change', 'lock_business')
    list_filter = ('business', 'darkMode', 'MFA', 'staff_change_First_password', 'force_password_Change', 'lock_business')
    search_fields = ('business', 'darkMode', 'MFA', 'staff_change_First_password', 'force_password_Change', 'lock_business')
    ordering = ('business',)
    
admin.site.register(Configuration, ConfigurationAdmin)