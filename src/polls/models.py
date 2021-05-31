from django.db import models


class Polls(models.Model):
    title = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

