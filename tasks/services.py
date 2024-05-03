from users.models import User
from django.db.models import Count
from django.contrib.auth.models import Group
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def sort_by_tasks():
    """Getting sorted queryset for model named User.
    The first step is to search for all users who don't belong to the group named Taskgiver.
    The second step is to exclude adminuser from user list.
    The next is the list by number of tasks."""
    group, created = Group.objects.get_or_create(name='Taskgiver')
    users = User.objects.exclude(groups=group)
    return users.filter(is_superuser=False).annotate(task_count=Count('tasks')).order_by('task_count')


def choose_executor(task):
    """This function allow us to find executor for chosen task.
    We iterate over all sorted users and select the user who has the least tasks or
    has a parent task."""
    users = list(sort_by_tasks())
    for user in users:
        if user.tasks:
            for job in user.tasks.all():
                if job == task.parent_task:
                    if user.tasks.all().count() - users[0].tasks.all().count() <= 2:
                        return user
    return users[0]


def send_mail_for_executor(task, user):
    """Function for sending email to executor to tell him about new task"""
    text = (f"Hello {user.fio}!\n"
            f"You have gotten one new task: {task.title}\n"
            f"{task.description}\n"
            f"Deadline is {task.term}")
    message = MIMEMultipart()
    message['Subject'] = "New task!"
    message.attach(MIMEText(text, 'plain'))
    connection = smtplib.SMTP(settings.EMAIL_HOST)
    connection.starttls()
    connection.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    connection.sendmail(from_addr=settings.EMAIL_HOST_USER, to_addrs=user.email, msg=message.as_string())
    connection.close()


def send_mail_for_taskgiver(task):
    """Function for sending email to taskgiver to tell him that task has been completed"""
    text = (f"Hello {task.owner}!\n"
            f"The task - {task.title} has been done\n")
    message = MIMEMultipart()
    message['Subject'] = "Report about completed task!"
    message.attach(MIMEText(text, 'plain'))
    connection = smtplib.SMTP(settings.EMAIL_HOST)
    connection.starttls()
    connection.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    taskgiver = User.objects.get(fio=task.owner)
    connection.sendmail(from_addr=settings.EMAIL_HOST_USER, to_addrs=taskgiver.email, msg=message.as_string())
    connection.close()
