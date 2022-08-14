from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
import datetime, time

# from https://stackoverflow.com/questions/25652809/django-file-upload-and-rename
# name each file starting with user id and add time stamp to the file name
# this will create unique file names and avoid overwrite
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.owner.id, str(int(time.time())), ext)
    return os.path.join('gallery', filename)

# class for managing users, extending from AbstractUser
class AppUser(AbstractUser):
    country = models.CharField(max_length = 100, null = False, blank = False)
    about_user = models.TextField(null = True, blank = True)
    contacts = models.ManyToManyField("AppUser", blank = True)
    photo = models.ImageField(upload_to='profile/', default='default/default_profile.png')

    # function to return profile photo (if it exists) or a default photo if one hasn't been loaded yet
    def get_photo(self):
        if self.photo:
            print('media/profile/' + str(self.photo))
            return settings.MEDIA_URL + str(self.photo)
        return settings.MEDIA_URL + self._meta.get_field('photo').get_default()

# class for status updates
class StatusUpdate(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "author", on_delete = models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add = True)
    content = models.TextField(null = False, blank = False)

# class for connection requests
class ConnectionRequest(models.Model):
    initiated_by = models.ForeignKey(AppUser, related_name = "initiated_by", on_delete = models.CASCADE)
    sent_to = models.ForeignKey(AppUser, related_name = "sent_to", on_delete = models.CASCADE)
    initiated_on = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 20, null = False, blank = False, default = 'pending')

# class for user's photo gallery
class UserPhoto(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "photo_owner", on_delete = models.CASCADE)
    added_on = models.DateTimeField(auto_now_add = True)
    photo = models.ImageField(blank = False, upload_to=content_file_name)