from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Task(models.Model):
    STATUS = (
        ('created', 'created'),
        ('worked', 'worked'),
        ('completed', 'completed'),
    )
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.CharField(max_length=200, verbose_name='description', **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='owned_tasks', verbose_name='owner', **NULLABLE)
    executor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='executed_tasks', verbose_name='executor', **NULLABLE)
    term = models.CharField(max_length=20, verbose_name='term')
    status = models.CharField(choices=STATUS, verbose_name='status', default='created')
    parent_task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='parent_task', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
