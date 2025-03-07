from django.contrib import admin
from .models import Subscription
# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('business', 'plan', 'expiry_date', 'amount', 'is_recurring', 'created_at', 'status', 'payment_status','cycle')
    list_filter = ('plan', 'is_recurring', 'created_at')
    search_fields = ('business', 'plan', 'expiry_date', 'amount', 'is_recurring', 'created_at')
    ordering = ('created_at',)

admin.site.register(Subscription, SubscriptionAdmin)
