from django.shortcuts import render
from rest_framework import status, generics, filters
from business.serializers.business_serializer import CreateBusinessSerializer, VerifyBusinessSerializer, GetBusinessSerializer
from rest_framework.response import Response
from .utils.gen_otp import generate_otp
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Business, Otp

# Create your views here.
class CreateBusinessView(generics.CreateAPIView):
    serializer_class = CreateBusinessSerializer

    def perform_create(self, serializer):
        business = serializer.save()
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