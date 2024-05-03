from rest_framework import serializers
from users.models import User
from users.validators import PhoneValidator


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user's views"""
    task_count = serializers.SerializerMethodField(source='test')

    def get_task_count(self, instance):
        return instance.tasks.count()

    class Meta:
        model = User
        fields = ['email', 'password', 'fio', 'position', 'phone', 'task_count', 'tasks']
        validators = [PhoneValidator(field='phone'), ]
