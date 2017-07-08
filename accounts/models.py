from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.

    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delHistoryDate = models.DateTimeField(blank=True, null=True, default=None)


    def __unicode__(self):
        return self.user.username
    