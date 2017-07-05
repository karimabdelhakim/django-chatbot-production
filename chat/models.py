from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from channels import Group
import json

class ChatMessage(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	message = models.CharField(max_length=255)
	owner = models.TextField(max_length=7)
	lineId = models.PositiveIntegerField(blank=True, null=True,default=None)
	character = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
	timestamp = models.DateTimeField(auto_now_add=True)

	@property
	def formatted_timestamp(self):
		return self.timestamp.strftime('%b %-d %-I:%M %p')

	@property
	def formatted_timestamp_milliseconds(self):
		seconds = self.timestamp.strftime('%s')	
		millisec = int(seconds)*1000
		return millisec

class BotMsgToAll(models.Model):
	staff = models.ForeignKey(settings.AUTH_USER_MODEL,limit_choices_to={'is_staff': True})
	message = models.CharField(max_length=255)
	owner = models.TextField(max_length=7, default='bot-all', editable=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	@property
	def formatted_timestamp(self):
		return self.timestamp.strftime('%b %-d %-I:%M %p')

	@property
	def formatted_timestamp_milliseconds(self):
		seconds = self.timestamp.strftime('%s')	
		millisec = int(seconds)*1000
		return millisec

@receiver(post_save, sender=BotMsgToAll)
def send_message(sender, instance, created, **kwargs):
	bot_msg = instance
	
	if created:

		final_msg = {
			"user":"",
			"msg": bot_msg.message,
			"owner": bot_msg.owner,
			"timestamp":bot_msg.formatted_timestamp
		}
		#send message to all users/all client types
		Group("all-users").send(
			{"text": json.dumps(final_msg)}
		)

