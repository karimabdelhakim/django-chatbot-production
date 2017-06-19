from channels import route
from .consumers import (ws_connect_api, ws_receive_api, ws_disconnect_api, 
    chat_send_api ,bot_send_api,chat_history_api)


# There's no path matching on these routes; we just rely on the matching
# from the top-level routing. We _could_ path match here if we wanted.
websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ws_connect_api),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive_api),

    # Called when WebSockets disconnect
    route("websocket.disconnect", ws_disconnect_api),
]


# You can have as many lists here as you like, and choose any name.
# Just refer to the individual names in the include() function.
custom_routing = [
    # Handling different chat commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    # route("chat.receive", chat_join, command="^join$"),
    # route("chat.receive", chat_leave, command="^leave$"),
    # route("chat.receive", chat_send, command="^send$"),
    route("chat-api.receive", chat_send_api, command="^send$"),
    route("chat-api.receive", chat_history_api, command="^history$"),
    route("bot-api.receive", bot_send_api),
]
