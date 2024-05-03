from rest_framework.serializers import ValidationError


class PhoneValidator:
    """Validator for field named phone"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        phone = value.get(self.field)
        if phone[:2] != "+7":
            raise ValidationError('Phone must have format: +7__________')
        if len(phone) != 12:
            raise ValidationError('Phone must be consisted of 12 characters')