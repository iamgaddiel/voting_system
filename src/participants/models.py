from django.db import models
from core.models import CustomUser
from polls.models import Polls


class Participant(models.Model):
    STACKS = [
        ('FrontEnd', 'FrontEnd'),
        ('BackEnd', 'BackEnd'),
        ('FullStack', 'FullStack'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    stack = models.CharField(max_length=30, choices=STACKS, default=STACKS[0])
    polls = models.ForeignKey(Polls, on_delete=models.CASCADE, null=True)
    

    def __str__(self) -> str:
        return f"participant {self.user.username}"
    