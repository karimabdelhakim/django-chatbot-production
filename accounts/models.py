from __future__ import unicode_literals
from django.conf import settings
from django.db import models
#from django.contrib.auth import get_user_model 
from django.db.models.signals import post_save
from django.dispatch import receiver

#User = get_user_model()

# Create your models here.

    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delHistoryDate = models.DateTimeField(blank=True, null=True, default=None)


    def __unicode__(self):
        return self.user.username
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def saveProfile(sender, instance, created, **kwargs):
	user = instance

	if created:
		Profile.objects.create(user=user)
