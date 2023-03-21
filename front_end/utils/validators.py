from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, DecimalValidator
from django.utils.translation import gettext_lazy as _


def validate_currency(value):
    MinValueValidator(0)(value)
    DecimalValidator(10, 2)(value)


def validate_first_char(value):
    if value[0] == '-':
        raise ValidationError(
            _('%(value)s , "-" karakteri ile başlayamaz.'),
            params={'value': value},
        )
