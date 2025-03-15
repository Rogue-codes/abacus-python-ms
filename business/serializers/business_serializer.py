from rest_framework import serializers
from business.models import Business
from django.contrib.auth.hashers import check_password

class GetBusinessSerializer(serializers.ModelField):
    class Meta:
        model = Business
        fields=['id','plan','first_name','last_name','business_name','email','phone','address','is_verified','is_active','role','currency']


class CreateBusinessSerializer (serializers.ModelSerializer):
    class Meta:
        model = Business
        fields=['plan','first_name','last_name','business_name','email','phone','address','password']


    def create(self, validated_data):
        return Business.objects.create(**validated_data) 
    
    
class VerifyBusinessSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)

class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)



class BusinessLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email").strip()
        password = data.get("password")

        # Check if business exists
        business = Business.objects.filter(email=email).first()
        if not business:
            raise serializers.ValidationError("Invalid credentials")

        # Verify password
        if not check_password(password, business.password):
            raise serializers.ValidationError("Invalid credentials")

        # Check if the account is active
        if not business.is_active:
            raise serializers.ValidationError("Account is inactive")

        data["business"] = business
        return data