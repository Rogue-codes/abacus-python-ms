from django.contrib import admin
from .models import Business, Employee

# Register your models here.
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'email', 'plan', 'is_verified', 'is_active', 'currency','id','phone')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'email', 'business', 'is_verified', 'is_active', 'salary','address','phone')

admin.site.register(Business, BusinessAdmin)
admin.site.register(Employee, EmployeeAdmin)