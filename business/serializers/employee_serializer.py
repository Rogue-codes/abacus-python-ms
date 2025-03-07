from rest_framework import serializers
from business.models import Employee
from plan.serializer import PlanSerializer

class GetBusinessSerializer(serializers.ModelField):
    class Meta:
        model = Employee
        fields=['id','modules','first_name','last_name','salary','email','phone','address','is_verified','is_active','business',]


class CreateEmployeeSerializer (serializers.ModelSerializer):
    # plan = PlanSerializer(source='business.plan', read_only=True)

    class Meta:
        model = Employee
        fields=['business','first_name','last_name','salary','email','phone','address','modules']