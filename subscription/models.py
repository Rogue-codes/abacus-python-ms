import uuid
from django.db import models
from plan.models import Plan
from business.models import Business

def get_default_plan():
    try:
        return Plan.objects.get(name="BASIC").id 
    except Plan.DoesNotExist:
        return None 

class Subscription(models.Model):
    class Status(models.TextChoices):
        IN_ACTIVE = "IN_ACTIVE"
        ACTIVE = "ACTIVE"
        EXPIRED = "EXPIRED"

    class PaymentStatus(models.TextChoices):
        NOT_PAID = "NOT_PAID"
        PAID = "PAID"

    class Cycle(models.TextChoices):
        YEARLY = "YEARLY"
        MONTHLY = "MONTHLY"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.SET_DEFAULT, default=get_default_plan, null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_recurring = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.IN_ACTIVE)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    cycle = models.CharField(max_length=10, choices=Cycle.choices, default=Cycle.MONTHLY)
    
    def __str__(self):
        return f"{self.business.business_name} - {self.plan.name} (Expires: {self.expiry_date})"
