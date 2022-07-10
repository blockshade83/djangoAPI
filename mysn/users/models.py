from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    # username = None
    email = models.EmailField(null = False, blank = False, unique = True)
    first_name = models.CharField(max_length = 50, null = False, blank = False)
    last_name = models.CharField(max_length = 100, null = False, blank = False)
    country = models.CharField(max_length = 100, null = False, blank = False)
    about_user = models.TextField(null = True, blank = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
