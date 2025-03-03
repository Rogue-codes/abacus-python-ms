from django.contrib import admin
from .models import Business
# Register your models here.
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'email', 'plan', 'is_verified', 'is_active', 'currency','id','phone')

admin.site.register(Business, BusinessAdmin)