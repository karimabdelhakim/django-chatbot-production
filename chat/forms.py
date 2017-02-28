from django import forms
from .models import BotMsgToAll

class MessageForm(forms.ModelForm):
	message = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = BotMsgToAll
		fields = [ "message"]