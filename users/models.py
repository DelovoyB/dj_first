from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        """
        Returns a string representation of the user object, which is its username.

        Returns:
            str: The username of the user.
        """
        return self.username