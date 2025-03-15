from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:business>/', views.GetConfigurationView.as_view(), name='get_configuration'),
    path('<uuid:business>/modify/', views.UpdateConfigurationView.as_view(), name='update_configuration'),
]