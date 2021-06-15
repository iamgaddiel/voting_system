from django.db import models
from django.utils import timezone
from core.models import CustomUser
from participants.models import ParticipantPolls
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
    judge = models.ForeignKey(JudgeProfile, on_delete=models.CASCADE)
    voted_participant = models.ForeignKey(ParticipantPolls, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(default=1)
    is_voted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=timezone.now)

    def __str__(self) -> str:
        return '{0} | voted: {1}'.format(
            self.judge.user.username,
            self.is_voted
        )
