from rest_framework import serializers
from business.models import Business

class GetBusinessSerializer(serializers.ModelField):
    class Meta:
        model = Business
        fields=['id','plan','first_name','last_name','business_name','email','phone','address','is_verified','is_active','role','currency']


class CreateBusinessSerializer (serializers.ModelSerializer):
    class Meta:
        model = Business
        fields=['plan','first_name','last_name','business_name','email','phone','address',]


    def create(self, validated_data):
        return Business.objects.create(**validated_data) 
    
    
class VerifyBusinessSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)