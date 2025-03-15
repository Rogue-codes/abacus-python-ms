import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from plan.models import Plan 
from django.utils.timezone import now
from modules.models import Module
from django.contrib.auth.hashers import make_password

def get_default_plan():
    return Plan.objects.get(name="BASIC").id 

class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.SET_DEFAULT, default=get_default_plan)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    business_name = models.CharField(max_length=50, blank=False, null=False,unique=True)
    email = models.EmailField(unique=True) 
    phone = models.CharField(max_length=12, blank=False, null=False, unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6)], blank=False, null=False)
    address = models.TextField(blank=False, null=False) 
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default="SUPER_ADMIN")
    currency = models.CharField(max_length=3, default="NGN")

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name


class Otp (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)  # Store the OTP code
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.email} - {self.code}"


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    modules = models.ManyToManyField(Module, related_name="employees")  # Many-to-Many Relationship
    email = models.EmailField() 
    phone = models.CharField(max_length=12, blank=False, null=False,)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(6)])
    address = models.TextField(blank=False, null=False) 
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    change_password = models.BooleanField(default=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.email