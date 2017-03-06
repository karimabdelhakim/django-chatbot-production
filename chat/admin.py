from django.contrib import admin

from .models import ChatMessage,BotMsgToAll
# Register your models here.

class ChatMessageModelAdmin(admin.ModelAdmin):
	list_display = ["message","timestamp","id","user"]
	list_display_links = ["timestamp"]
	list_filter = ["timestamp"]
	ordering = ['timestamp']
	search_fields = ['user__username']
	class Meta:
		model = ChatMessage


admin.site.register(ChatMessage, ChatMessageModelAdmin)

class BotMsgToAllModelAdmin(admin.ModelAdmin):
	list_display = ["message","timestamp","id","staff"]
	list_display_links = ["timestamp"]
	list_filter = ["timestamp"]
	ordering = ['timestamp']
	class Meta:
		model = BotMsgToAll

admin.site.register(BotMsgToAll, BotMsgToAllModelAdmin)