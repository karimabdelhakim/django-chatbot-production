from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import ChatMessage,BotMsgToAll
from .forms import MessageForm
from itertools import chain
from operator import attrgetter


@login_required
def index(request):
    
    #user and bot messages sent to the specific user
    chat_msgs_qs = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    #bot messages sent to all existing users
    bot_msgs_qs = BotMsgToAll.objects.filter(timestamp__gt=request.user.date_joined).order_by('timestamp')
    #joining the two list querysets into one sorted list queryset.
	#sorted by timestamp, can be sorted by -timestamp if 
	#reverse=True argument is added after key like in the api view
    result_list = sorted(chain(chat_msgs_qs,bot_msgs_qs),key=attrgetter('timestamp'))
    
    return render(request, "index.html", {
        "messages": result_list,
    })

@login_required
def message_to_all(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise PermissionDenied   
    form = MessageForm(request.POST or None)
    if form.is_valid() and request.user.is_staff:
        instance = form.save(commit=False)
        instance.staff = request.user
        instance.save()
        messages.success(request, "Message Successfully Sent")
        return HttpResponseRedirect(reverse("broadcast"))
    title = 'send message'    
    return render(request,"registration/form.html",{"form":form,"title":title})
