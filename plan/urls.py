from django.urls import path
from . import views

urlpatterns = [
    path('all', views.PlanListView.as_view()),
]