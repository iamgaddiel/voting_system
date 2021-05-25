from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ACCOUNT_TYPE = [
        ('competitor', 'competitor'),
        ('judge', 'judge'),
    ]
    id =  models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    account_type = models.CharField(choices=ACCOUNT_TYPE, max_length=10)


    def __str__(self) -> str:
        return '{0} {1} {2}'.format(self.username, self.first_name, self.last_name)