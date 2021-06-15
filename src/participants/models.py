from django.db import models
from django.utils import timezone
from core.models import CustomUser
from polls.models import Polls

import uuid

class Participant(models.Model):
    STACKS = [
        ('FrontEnd', 'FrontEnd'),
        ('BackEnd', 'BackEnd'),
        ('FullStack', 'FullStack'),
    ]
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stack = models.CharField(max_length=30, choices=STACKS, default=STACKS[0])
    

    def __str__(self) -> str:
        return f"participant | {self.user.username}"
    
class ParticipantPolls(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    polls = models.ForeignKey(Polls, on_delete=models.CASCADE)
    project_link = models.CharField(max_length=100, blank=True, default='')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    vote_count = models.PositiveIntegerField(default=0)
    is_uploaded = models.BooleanField(default=False)
    total_rating = models.PositiveIntegerField(default=0, blank=True, help_text="total nuber of rating")
    timestamp = models.DateTimeField(auto_now=timezone.now)

    def __str__(self) -> str:
        return '{0} | total rating: {1}'.format(
            self.participant.user.username,
            self.total_rating
        )
    
    def get_avarage_rating(self):
        avarage = 0 if self.vote_count == 0 else self.total_rating / self.vote_count
        return avarage

    class Meta:
        ordering = ['-total_rating']
