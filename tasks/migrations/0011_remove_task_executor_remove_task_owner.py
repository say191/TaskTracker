# Generated by Django 4.2.7 on 2024-05-06 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_alter_task_executor_alter_task_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        migrations.RemoveField(
            model_name='task',
            name='owner',
        ),
    ]
