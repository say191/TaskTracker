from tasks.apps import TasksConfig
from django.urls import path
import tasks.views as v

app_name = TasksConfig.name

urlpatterns = [
    path('', v.TaskListAPIView.as_view(), name='tasks_list'),
    path('create/', v.TaskCreateAPIView.as_view(), name='task_create'),
    path('<int:pk>/', v.TaskRetrieveAPIView.as_view(), name='task_get'),
    path('update/<int:pk>/', v.TaskUpdateAPIView.as_view(), name='task_update'),
    path('delete/<int:pk>/', v.TaskDestroyAPIView.as_view(), name='task_delete'),
    path('find_exe/<int:pk>/', v.FindExecutorAPIView.as_view(), name='find_exe'),
    path('done/<int:pk>/', v.TaskIsDoneAPIView.as_view(), name='task_done'),
    path('important_tasks/', v.ImportantTasksAPIView.as_view(), name='important_tasks')
]
