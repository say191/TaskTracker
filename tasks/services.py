from users.models import User
from django.db.models import Count
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from tasks.models import Task


def sort_by_tasks():
    """Getting sorted queryset for model named User.
    The first step is to search for all users who don't belong to the group named Taskgiver.
    The second step is to exclude adminuser from user list.
    The next is the list by number of tasks."""
    users = User.objects.exclude(groups__name='Taskgiver')
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


def send_mail_for_executor(task):
    """Function for sending email to executor to tell him about new task"""
    text = (f"Hello {task.executor.fio}!\n"
            f"You have gotten one new task: {task.title}\n"
            f"{task.description}\n"
            f"Deadline is {task.term}")
    message = MIMEMultipart()
    message['Subject'] = "New task!"
    message.attach(MIMEText(text, 'plain'))
    connection = smtplib.SMTP(settings.EMAIL_HOST)
    connection.starttls()
    connection.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    connection.sendmail(from_addr=settings.EMAIL_HOST_USER, to_addrs=task.executor.email, msg=message.as_string())
    connection.close()


def send_mail_for_taskgiver(task):
    """Function for sending email to taskgiver to tell him that task has been completed"""
    text = (f"Hello {task.owner.fio}!\n"
            f"The task - {task.title} has been done\n")
    message = MIMEMultipart()
    message['Subject'] = "Report about completed task!"
    message.attach(MIMEText(text, 'plain'))
    connection = smtplib.SMTP(settings.EMAIL_HOST)
    connection.starttls()
    connection.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
    connection.sendmail(from_addr=settings.EMAIL_HOST_USER, to_addrs=task.owner.email, msg=message.as_string())
    connection.close()


def get_important_tasks():
    """Function for getting list of strings consisted from important tasks (linked tasks)
    and users who can do this important tasks. The func iterates all tasks with created status
    and then iterates all users in sorted list by count of tasks to choose users with parent task and
    condition (the least busy employee or an employee performing a parent task if he is assigned
    a maximum of 2 more tasks than the least busy employee)"""
    users = list(sort_by_tasks())
    tasks = list(Task.objects.filter(status='created'))
    results = []
    for task in tasks:
        if task.parent_task:
            employees = []
            for user in users:
                if task.parent_task in user.tasks.all():
                    if user.tasks.all().count() - users[0].tasks.all().count() <= 2:
                        employees.append(user)
            if len(employees) ==0:
                employees.append(users[0])
            results.append(f"{task} - {task.term} - {employees}")
    return results
