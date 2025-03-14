from rest_framework import serializers
from .models import Subscription
from business.models import Business
class GetSubcriptionSerializer(serializers.ModelField):
    class Meta:
        model = Subscription
        fields=['business', 'plan', 'expiry_date', 'is_reocurring', 'created_at', 'status', 'payment_status', 'cycle']

class CreateSubscriptionSerializer(serializers.ModelSerializer):
    business_email = serializers.EmailField(write_only=True)  # Accept email input

    class Meta:
        model = Subscription
        fields = ['business_email', 'plan', 'is_reocurring', 'cycle']  # Replace 'business' with 'business_email'

    def validate_business_email(self, value):
        """Check if the email exists and return the corresponding Business instance."""
        try:
            business = Business.objects.get(email=value)
        except Business.DoesNotExist:
            raise serializers.ValidationError("No business found with this email.")
        return business

    def create(self, validated_data):
        """Replace 'business_email' with the actual Business instance."""
        business = validated_data.pop('business_email')  # Retrieve validated business object
        validated_data['business'] = business  # Assign the Business instance
        return Subscription.objects.create(**validated_data)
