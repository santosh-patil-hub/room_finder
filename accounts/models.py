from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import AbstractUser



LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('owner', 'Owner'),
        ('tenant', 'Tenant'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='tenant')

    def __str__(self):
        return f"{self.username} ({self.user_type})"

