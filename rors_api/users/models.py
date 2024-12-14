from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
    )

    role = models.CharField(max_length=10, choices=ROLES, default='teacher')

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.get_full_name() ({self.role})}"
