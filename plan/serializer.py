from .models import Plan
from rest_framework import serializers

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'features', 'price', 'modules', 'currency'] 