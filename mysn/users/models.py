from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class AppUser(AbstractUser):
    # email = models.EmailField(null = False, blank = False, unique = True)
    # first_name = models.CharField(max_length = 50, null = False, blank = False)
    # last_name = models.CharField(max_length = 100, null = False, blank = False)
    country = models.CharField(max_length = 100, null = False, blank = False)
    # is_active = models.BooleanField(default=True)
    about_user = models.TextField(null = True, blank = True)

    # objects = AppUserManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

class StatusUpdate(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add = True)
    content = models.TextField(null = False, blank = False)

