from django.db import models


class Polls(models.Model):
    title = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300, blank=True, unique=True)
    # start_date = models.DateField()
    # start_time = models.TimeField(null=True)
    # end_date = models.DateField()
    # end_time = models.TimeField(null=True)
    is_active = models.BooleanField(default=True, help_text="mark poll as open")

    def __str__(self) -> str:
        return "{0} | {1}".format(self.title, self.address)

    def save(self, *args, **kwargs):
        import shortuuid
        self.address = shortuuid.ShortUUID().random(length=22)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']