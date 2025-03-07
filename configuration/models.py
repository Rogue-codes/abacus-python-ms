import uuid
from django.db import models
from business.models import Business
# Create your models here.
class Configuration (models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    business= models.ForeignKey(Business, on_delete=models.CASCADE)
    darkMode= models.BooleanField(default=False)
    MFA= models.BooleanField(default=False)
    staff_change_First_password= models.BooleanField(default=False)
    force_password_Change = models.BooleanField(default=False)
    lock_business= models.BooleanField(default=False)


    def __str__(self):
        return self.id