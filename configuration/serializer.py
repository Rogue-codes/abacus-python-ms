from .models import Configuration
from rest_framework import serializers

class ConfigurationSerializer (serializers.ModelSerializer):
    class Meta:
        model=Configuration
        fields=['darkMode', 'MFA', 'staff_change_First_password', 'force_password_Change', 'lock_business']