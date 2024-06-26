# Generated by Django 4.2.7 on 2024-05-06 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0012_task_executor_task_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executed_tasks', to=settings.AUTH_USER_MODEL, verbose_name='executor'),
        ),
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
