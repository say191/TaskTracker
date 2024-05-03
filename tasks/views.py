from rest_framework.viewsets import generics
from rest_framework.views import APIView
from tasks.serializers import TaskSerializer
from tasks.models import Task
from tasks.services import choose_executor, send_mail_for_executor, send_mail_for_taskgiver
from users.permissions import IsTaskgiver, IsOwnerForTask
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group


class TaskCreateAPIView(generics.CreateAPIView):
    """View for creating task"""
    serializer_class = TaskSerializer
    permission_classes = [IsTaskgiver, ]

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.owner = self.request.user.fio
        new_task.save()


class TaskListAPIView(generics.ListAPIView):
    """View for displaying all of tasks"""
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsTaskgiver | IsAdminUser, ]


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    """View for displaying one chosen task"""
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsOwnerForTask | IsAdminUser, ]


class TaskUpdateAPIView(generics.UpdateAPIView):
    """View for updating one chosen task"""
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsOwnerForTask | IsAdminUser, ]


class TaskDestroyAPIView(generics.DestroyAPIView):
    """View for deleting one chosen task"""
    queryset = Task.objects.all()
    permission_classes = [IsOwnerForTask | IsAdminUser, ]


class FindExecutorAPIView(APIView):
    """View for searching executor for task"""
    permission_classes = [IsTaskgiver, ]

    def get(self, request, pk):
        try:
            task = Task.objects.filter(status='created').get(id=pk)
            user = choose_executor(task)
            task.executor = user.fio
            task.status = 'worked'
            task.save()
            user.tasks.add(task)
            group, created = Group.objects.get_or_create(name='Executor')
            user.groups.add(group)
            user.save()
            send_mail_for_executor(task, user)
            return Response({'message': f'{task.title} - {task.term} - {task.executor}.'}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "This task not found"}, status=status.HTTP_404_NOT_FOUND)


class TaskIsDoneAPIView(APIView):
    """View to mark this task as done"""
    permission_classes = [IsOwnerForTask | IsTaskgiver, ]

    def get(self, request, pk):
        try:
            user = request.user
            task = user.tasks.all().get(id=pk)
            task.status = 'completed'
            task.save()
            user.tasks.remove(task)
            user.save()
            send_mail_for_taskgiver(task)
            return Response({'message': 'The task is marked as completed'}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'This task not found'}, status=status.HTTP_404_NOT_FOUND)
