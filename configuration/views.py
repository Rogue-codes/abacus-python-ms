from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .models import Configuration  # Your model
from .serializer import ConfigurationSerializer 

# Create your views here.
class GetConfigurationView(RetrieveAPIView):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    lookup_field = 'business'

    def get(self, request, business, *args, **kwargs):
        """
        Retrieve a single configuration by business id.
        """

        configuration = get_object_or_404(Configuration, business=business)
        print("configuration", model_to_dict(configuration))
        serializer = self.get_serializer(configuration)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateConfigurationView (UpdateAPIView):
    queryset = Configuration.objects.all()
    serializer_class= ConfigurationSerializer
    lookup_field='business'

    def patch(self, request, business, *args, **kwargs):
        configuration = get_object_or_404(Configuration, business=business)
        serializer = self.get_serializer(configuration, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
