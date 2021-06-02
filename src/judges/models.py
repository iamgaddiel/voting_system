from django.db import models
from django.utils import timezone
from core.models import CustomUser
from polls.models import Polls
import uuid


class JudgeProfile(models.Model):
    QUALIFICATION = [
        ('ND', 'ND'),
        ('HND', 'HND'),
        ('BSC', 'BSC'),
        ('MSc', 'MSc'),
        ('Phd', 'Phd'),
    ]
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="judges_profile_picture", default="profile.png")
    educational_qualification = models.CharField(max_length=20, choices=QUALIFICATION)

    def __str__(self) -> str:
        return f"{self.user.username} profile"

class JudgesPoll(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    polls = models.ForeignKey(Polls, on_delete=models.CASCADE)
    project_link = models.CharField(max_length=100, blank=True, default='')
    judge = models.ForeignKey(JudgeProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=timezone.now)

    def __str__(self) -> str:
        return '{0}'.format(self.judge.user.username)
