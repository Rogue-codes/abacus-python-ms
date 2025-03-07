from rest_framework import serializers
from .models import Subscription

class GetSubcriptionSerializer(serializers.ModelField):
    class Meta:
        model = Subscription
        fields=['business', 'plan', 'expiry_date', 'is_recurring', 'created_at', 'status', 'payment_status', 'cycle']


class CreateSubcriptionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields=['business', 'plan', 'is_recurring','cycle']