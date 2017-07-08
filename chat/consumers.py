import json
from django import forms
from channels import Channel,Group
# from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user

from .models import ChatMessage


from botlogic.Lina.Lina import callBot


# Connected to chat.receive channel
# chat_send is chat.receive channel consumer
@channel_session_user
def chat_send(message):
    print("chat_send")
    owner = "user"
    user = message.user #dont forget to check if user exist in DB 
    msg = message.content['message']
    field = forms.CharField()
    if not (field.clean(msg)):
        raise forms.ValidationError("Message can not be empty")
    msg = field.clean(msg)         
    # Save to model
    msg_obj = ChatMessage.objects.create(
        user = user,
        message = msg,
        owner = owner
    )
    if(msg_obj):
        final_msg = {
            "user":msg_obj.user.username,
            "msg": msg_obj.message,
            "owner": msg_obj.owner,
            "timestamp":msg_obj.formatted_timestamp
        }
    else:
        final_msg = {
            "user":user.username,
            "msg": "sorry ,DB error",
            "owner": owner,    
        }    
    #print("final_msg",final_msg)
    # Broadcast to listening socket(send user message to the user himself)
    message.reply_channel.send({"text": json.dumps(final_msg)})

    #bot listening logic
    payload = {
        'reply_channel': message.content['reply_channel'],
        'message': msg,
        'character':message.content['character'],
    }
    Channel("bot.receive").send(payload)


# Connected to bot.receive channel
# bot_send is bot.receive channel consumer
# bot consumer 
@channel_session_user
def bot_send(message):
    print("bot_send")
    owner = "bot"
    user = message.user 
    msg = message.content['message']
    character = message.content['character']
    #bot logic
    response_type,response =callBot(msg,character)
    
    if(response_type=="message"):
        msg = response[0]
        dataset_number = response[1]
        line_id = response[2]
    
    elif(response_type=="intent"):
        msg = ""
        dataset_number = None
        line_id = None
            
    msg_obj = ChatMessage.objects.create(
        user = user,
        message = msg,
        owner = owner,
        lineId = line_id,
        character = dataset_number
    )
    if(msg_obj):
        final_msg = {
                "user":msg_obj.user.username,
                "msg": msg_obj.message,
                "owner": msg_obj.owner,
                "type":response_type,
                "data":response,
                "line_id":msg_obj.lineId,
                "msg_id":msg_obj.id,
                "timestamp":msg_obj.formatted_timestamp,
                "formated_timestamp":msg_obj.formatted_timestamp_milliseconds
        }
        
    else:
        final_msg = {
            "user":user.username,
            "msg": "sorry ,DB error",
            "owner": owner,    
        }  
    print("final_msg",final_msg)
    #print("final_msg",final_msg)
    # Broadcast to listening socket(send bot reply message to the user)
    message.reply_channel.send({"text": json.dumps(final_msg)})





# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    print("ws_connect")
    # Accept connection
    message.reply_channel.send({"accept": True})
    #add each user to all-users group when they connect,
    #so that they can recieve any bot announce message. 
    Group("all-users").add(message.reply_channel)
    


# Connected to websocket.receive
def ws_receive(message):
    print("ws_receive")
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    #print(message['text'],payload)

    # Stick the message onto the processing queue
    Channel("chat.receive").send(payload)

# Connected to websocket.disconnect
def ws_disconnect(message):
    print("ws_disconnect")
    #remove each user from all-users group when they disconnect.
    Group("all-users").discard(message.reply_channel)