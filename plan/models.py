import uuid
from django.db import models

# Create your models here.
class Plan(models.Model):
    id=models.UUIDField(primary_key=True, default = uuid.uuid4)       
    name= models.CharField(max_length=50, unique=True, blank=False, null=False)
    features= models.JSONField()
    currency= models.CharField(max_length=3, default="NGN", blank=False, null=False)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    