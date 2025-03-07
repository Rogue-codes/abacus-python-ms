from django.shortcuts import render
from rest_framework import status, generics, filters,serializers
from business.serializers.employee_serializer import CreateEmployeeSerializer
from rest_framework.response import Response
from .utils.gen_sys_password import generate_sys_password
from django.utils.timezone import now
from .models import Employee, Business
from plan.models import Plan
from django.core.mail import send_mail
from .utils.send_employee_email import send_employee_email
from django.forms.models import model_to_dict


class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = CreateEmployeeSerializer

    def perform_create(self, serializer):
        business = Business.objects.get(business_name=serializer.validated_data["business"])
        plan = model_to_dict(Plan.objects.get(name=business.plan))
        modules = serializer.validated_data["modules"]
        
        plan_modules = [str(module) for module in plan['modules']]
    
    # Validate each requested module
        for module in modules:
            if str(module) not in plan_modules:
                raise serializers.ValidationError({
                "modules": f"Plan does not support module: {module}"
            })
        
        if not business.is_verified and not business.is_active:
            raise serializers.ValidationError({"business": "Business is not verified or active"})
        system_generated_password = generate_sys_password()
        employee = serializer.save(password=system_generated_password)

        send_employee_email(employee, system_generated_password, business.business_name)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": "Employee created successfully",
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )