from rest_framework.generics import ListAPIView
from .models import Plan
from .serializer import PlanSerializer
from rest_framework.response import Response

class PlanListView(ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Plans retrieved successfully",
            "data": serializer.data
        })