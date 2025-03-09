from django.shortcuts import render
from rest_framework import status, generics, filters
from business.serializers.business_serializer import CreateBusinessSerializer, VerifyBusinessSerializer, BusinessLoginSerializer, ResendOtpSerializer
from rest_framework.response import Response
from .utils.gen_otp import generate_otp
from django.utils.timezone import now
from .models import Business, Otp
from configuration.models import Configuration
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.forms.models import model_to_dict
from plan.models import Plan
# Create your views here.
class CreateBusinessView(generics.CreateAPIView):
    serializer_class = CreateBusinessSerializer

    def perform_create(self, serializer):
        business = serializer.save()
        Configuration.objects.create(business=business)
        generate_otp(business.email)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": "business created successfully",
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )
    

class VerifyBusinessView(generics.GenericAPIView):
    serializer_class = VerifyBusinessSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]

        try:
            business = Business.objects.get(email=email)
            otp_instance = Otp.objects.filter(email=email, code=otp_code).first()

            if not otp_instance:
                return Response({"success": False, "message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            if otp_instance.expires_at < now():
                return Response({"success": False, "message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Verify and activate Business
            business.is_active = True
            business.is_verified = True

            business.save()
            

            # Delete used OTP
            otp_instance.delete()

            return Response({"success": True, "message": "Business verified successfully."}, status=status.HTTP_200_OK)

        except Business.DoesNotExist:
            return Response({"success": False, "message": "Business not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ResendOtp(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            business = Business.objects.get(email=email)
            if business.is_verified == True:
                return Response({"success": False, "message": "Business is already verified."}, status=status.HTTP_400_BAD_REQUEST)
            generate_otp(email)
            return Response({"success": True, "message": "OTP sent successfully."}, status=status.HTTP_200_OK)

        except Business.DoesNotExist:
            return Response({"success": False, "message": "Business not found."}, status=status.HTTP_404_NOT_FOUND)


class BusinessLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = BusinessLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            business = serializer.validated_data["business"]
            refresh = RefreshToken.for_user(business)

            plan = model_to_dict(Plan.objects.get(name=business.plan))
            modules = [str(module) for module in plan["modules"]]
 

            return Response({
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "business": {
                    "id": str(business.id),
                    "first_name": business.first_name,
                    "last_name": business.last_name,
                    "business_name": business.business_name,
                    "email": business.email,
                    "phone": business.phone,
                    "is_verified": business.is_verified,
                    "is_active": business.is_active,
                    "currency": business.currency,
                    "modules": modules,
                    "plan": str(business.plan)
                },            
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)