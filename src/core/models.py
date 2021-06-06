from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    id =  models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=GENDER, default=GENDER[0])
    dob = models.DateField(null=True)
    is_participant = models.BooleanField(default=False)
    is_judge = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    def __str__(self) -> str:
        return 'username: {0} | {1} {2}'.format(self.username, self.first_name, self.last_name)

    # def get_absolute_url(self):
    #     pass
    
    class Profile(models.Model):
        user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
        image = models.ImageField(upload_to="profile-images", default="profile.png")

        def __str__(self) -> str:
            return "{0} profile".format(self.user)
