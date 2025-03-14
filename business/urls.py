from django.urls import path
from . import views, employee_view

urlpatterns = [
    path('register', views.CreateBusinessView.as_view()),
    path('verify', views.VerifyBusinessView.as_view()),
    path('resend-otp', views.ResendOtp.as_view()),
    path('create-employee', employee_view.CreateEmployeeView.as_view()),
    path('login', views.BusinessLoginView.as_view(), name=""),
    # path('<uuid:id>/activate', views.ActivateTenantView.as_view()),
    # path('task/create/', views.CreateTaskApiview.as_view()),
    # path('tasks/all/', views.MyTaskListApiView.as_view(), name='tasks_list'),
    # path('tasks/<uuid:task_id>', views.TaskDetailsView.as_view(), name='task'),
    # path("tasks/<uuid:task_id>/status/",
    #      views.UpdateTaskStatusView.as_view(), name="update_task_status"),
    # path("tasks/<uuid:task_id>/update/",
    #      views.UpdateTaskView.as_view(), name="update_task"),
]
