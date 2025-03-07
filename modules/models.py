import uuid
from django.db import models

# Create your models here.
class Module (models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=100, unique=True)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Permission (models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    name=models.CharField(max_length=100, unique=True)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
