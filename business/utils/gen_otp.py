# utils/genOtp.py
from datetime import timedelta
from django.core.mail import send_mail
from django.utils.timezone import now
from business.models import Otp
import random

def generate_otp(email):
    """Generate and store OTP"""
    otp_code = str(random.randint(100000, 999999))
    expiry_time = now() + timedelta(minutes=5)
    
    send_mail(
        "Your Verification Code",
        f"Your OTP code is: {otp_code}",
        "eduarc4life@gmail.com",
        [email],
        fail_silently=False,
    )
    
    otp, created = Otp.objects.update_or_create(
        email=email,
        defaults={"code": otp_code, "expires_at": expiry_time}
    )
    return otp_code