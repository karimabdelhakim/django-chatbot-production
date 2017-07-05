import re

### These are the regex that we are going to use
set_alarm_regex = r"([Ss]et\s+[Aa]larm\s+([\D ]*)((\d{1,2}):?(\d{0,2}))?)"

call_number_regex = r"([Cc]all\s+\+?([0-9\s-]){3,})"
view_contact_regex = r"([Vv]iew\s+contact\s+([A-Z0-9]\w*[\s\.]?)+)"
call_contact_regex = r"([Cc]all\s+([A-Z0-9]\w*[\s\.]?)+)"

send_email_regex = r"([Ss]end\s+[Ee]mail\s+to\s+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\s?(\[.*\])?\s(\[.*\]))"

set_event_regex = r"([Ss]et\s+[Ee]vent\s+(\d{4}:\d{1,2}:\d{1,2}:?\d{0,2}:?\d{0,2})\s*(\d{4}:\d{1,2}:\d{1,2}:?\d{0,2}:?\d{0,2})?\s+(\[[\w ,_]*\])\s*(\[[\w ,_]*\])?\s*(\[[\w ,_]*\])?)"

message_contact_regex = r"([Ss]end\s+[Mm]essage\s+[Tt]o\s+(([A-Z0-9]\w*[\s\.]?)+)(\[.*\]))"
message_number_regex = r"([Ss]end\s+[Mm]essage\s+[Tt]o\s+\+?([0-9\s-]{3,})\s?(\[.*\]))"

start_timer_regex = r"([Ss]tart\s+(\d{1,2}):?(\d{0,2})\s+[Tt]imer)"

save_note_regex = r"([Ss]ave\s+[Nn]ote\s+(\[[\w ,_]*\])\s*(\[[\w ,_]*\])?)"
show_note_regex = r"([Ss]how\s+(.*)\s+[Nn]ote)"
edit_note_regex = r"([Ee]dit\s+[Nn]ote\s+(\[.*\])\s+(\[.*\]))"
delete_note_regex = r"([Dd]elete\s+[Nn]ote\s+(\[.*\]))"


###

########################## set_alarm ##########################
def trim(text):
    if len(text) <= 1:
        return ""
    ending_marks = "."
    if text[-1] in ending_marks:
        return trim(text[:-1].strip())
    elif text[0] in ending_marks:
        return trim(text[1:].strip())
    else:
        return text.strip()


# text ="""
#       set alarm morning alarm for 10:30
#       Set alarm 10:00
#       Set alarm 12-20 it causes an error
#       Set alarm 10
#       Set alarm 1:1
#       set alarm any_name
#   """
def default(par, value):
    if len(par) == 0:
        return str(value)
    else:
        return par


def get_set_alarm(text):
    match = re.search(set_alarm_regex, text)
    output = []
    if match:
        matches = re.findall(set_alarm_regex, text)

        for match in matches:
            output.append(("set_alarm", "title(\'" + trim(match[1]) + "\')", \
                           "hour(\'" + default(match[3], 0) + "\')", \
                           "minute(\'" + default(match[4], 0) + "\')"))

    return output


########################## call_number ##########################
# text = """
#       call 011 27 55 70 54
#       call 013 27 55 70 54
#       call 2010-6-12-51-0-93
#       call +2011 287. very soon
#       call 1. please, call +01 it's urgent.
#       """
def trim_number(text):
    marks = "\t\n .-_"
    output = ""
    if text == "":
        return text

    for ch in text:
        if ch in marks:
            pass
        else:
            output += ch
    return output


def get_call_number(text):
    match = re.search(call_number_regex, text)
    output = []
    if match:
        matches = re.findall(call_number_regex, text)
        for match in matches:
            num = trim_number(match[0][5:])
            output.append(("call_number", "number(\'" + num + "\')"))

    return output


########################## view_contact ##########################
# text = "please, View contact Mohamed Anwar and View contact Mo7amed Gamal. \
# Don't forget to view contact M.Mostafa Elafasay and view contact Amr 3ezzat \
# and View amr info, or view Amr Diab Info"


def get_view_contact(text):
    match = re.search(view_contact_regex, text)
    output = []
    if match:
        matches = re.findall(view_contact_regex, text)
        for match in matches:
            output.append(("view_contact", "contact_name(\'" + trim(match[0][13:]) + "\')"))

    another_regex = r"([Vv]iew\s+(([A-Z0-9]\w*[\s\.]?)+)\s*[Ii]nfo)"
    match = re.search(another_regex, text)
    if match:
        matches = re.findall(another_regex, text)
        for match in matches:
            output.append(("view_contact",
                           "contact_name(\'" + trim(match[1]) + "\')"))
    return output


########################## call_contact ##########################
# text = "please, call Mohamed Anwar and Call Mo7amed Gamal.\
# Don't forget to call M.Mostafa Elafasay and call Amr 3ezzat"
def delete_white_space(text):
    white_space = "\t\n "
    output = ""
    if text == "":
        return text

    for ch in text:
        if ch in white_space:
            pass
        else:
            output += ch
    return output


def get_call_contact(text):
    match = re.search(call_contact_regex, text)
    output = []
    if match:
        matches = re.findall(call_contact_regex, text)
        for match in matches:
            temp = delete_white_space(match[0][5:])
            if trim(temp).isdigit():
                pass
            else:
                output.append(("call_contact", "contact_name(\'" + trim(match[0][5:]) + "\')"))

    return output


########################## send_email ##########################
# text = """
#       try to send email to mohamed.anwar_vic@gmail.com [job offer] [You are totally rejected]
#       let's Send email to eagle_start2010@yahoo.com [we are going to be OK [now, we are not], isA]
#       send email [no] [noo]
#       send email to m@h.com []
#       """

def get_send_email(text):
    match = re.search(send_email_regex, text)
    output = []
    if match:
        matches = re.findall(send_email_regex, text)

        for match in matches:
            output.append(("send_email", "email(\'" + trim(match[1]) + "\')", \
                           "subject(\'" + match[2][1:-1] + "\')", \
                           "body(\'" + match[3][1:-1] + "\')"))

    return output


########################## set_event ##########################
# text = """
#       set event     2017:8:01:14:00           2017:8:01:14:00       [title] [des] [location]
#       set event 2017:8:14:17:32        [title] [description]
#       set event 2087:8:30        [location]
#       set event 2117:8:1        []
#       Set event 12:3:4 []
#         Set event 2:10 10:11 [title]
#         Set event 22:00 [title]
#       """

def get_set_event(text):
    match = re.search(set_event_regex, text)
    output = []
    if match:
        matches = re.findall(set_event_regex, text)
        for match in matches:
            output.append(("set_event", \
                           "start_time(\'" + match[1] + "\')", \
                           "end_time(\'" + default(match[2], 0) + "\')", \
                           "title(\'" + match[3][1:-1] + "\')", \
                           "text(\'" + match[4][1:-1] + "\')", \
                           "location(\'" + match[5][1:-1] + "\')"))
    another_regex = r"([Ss]et\s+[Ee]vent\s+(\d{0,2}:\d{0,2})\s*(\d{0,2}:\d{0,2})?\s+(\[[\w ,_]*\])\s*(\[[\w ,_]*\])?\s*(\[[\w ,_]*\])?)"
    match = re.search(another_regex, text)
    if match:
        matches = re.findall(another_regex, text)
        for match in matches:
            output.append(("set_event", \
                           "start_time(\'" + match[1] + "\')", \
                           "end_time(\'" + default(match[2], 0) + "\')", \
                           "title(\'" + match[3][1:-1] + "\')", \
                           "text(\'" + match[4][1:-1] + "\')", \
                           "location(\'" + match[5][1:-1] + "\')"))

    return output


########################## message_contact ##########################
# text = """
#       send message to Amr 3zzat [How are you?]
#       Send message to M.Anwar[How are you?]
#       send message to m.Anwar [How are you?]
#       Send message to Anwar[][]
#         send message to 011 [How are you?]
#       """
def get_message_contact(text):
    match = re.search(message_contact_regex, text)
    output = []
    if match:
        matches = re.findall(message_contact_regex, text)
        for match in matches:
            temp = delete_white_space(trim(match[1]))
            if trim(temp).isdigit():
                pass
            else:
                output.append(("message_contact", \
                               "contact_name(\'" + trim(match[1]) + "\')", \
                               "message(\'" + match[3][1:-1] + "\')"))

    return output


########################## message_number ##########################
# text = """
#       send message to 011 []
#       send message to 011 27 55 70 54[][][][][
#       Send message to 01127557066u98[please, call me back. It's urgent]
#       send message to 3zzat [How are you?]
#       Send message to 1 [][]
#       Send message to 11 [][]
#       """

def get_message_number(text):
    match = re.search(message_number_regex, text)
    output = []
    if match:
        matches = re.findall(message_number_regex, text)
        for match in matches:
            output.append(("message_number", \
                           "number(\'" + trim_number(match[1]) + "\')", \
                           "message(\'" + match[2][1:-1] + "\')"))

    return output


########################## start_timer ##########################
# text ="""
#       start timer morning alarm 10:30
#       start timer 10:00
#       start timer 12-20 it causes an error
#       start 10 timer
#       start 1:1 timer
#       start timer now
#       start now timer
#   """

def get_start_timer(text):
    match = re.search(start_timer_regex, text)
    output = []
    if match:
        matches = re.findall(start_timer_regex, text)
        for match in matches:
            output.append(("start_timer", "minute(\'" + default(match[1], 0) + "\')", \
                           "second(\'" + default(match[2], 0) + "\')"))

    return output


########################## save_note ##########################
# text = """
#       try to Save note [job offer] [You are totally rejected]
#       let's save note [we are going to be OK [now, we are not], isA]
#       Save note [no] [noo]
#       """

def get_save_note(text):
    match = re.search(save_note_regex, text)
    output = []
    if match:
        matches = re.findall(save_note_regex, text)
        for match in matches:
            output.append(("save_note", "title(\'" + match[1][1:-1] + "\')", \
                           "text(\'" + match[2][1:-1] + "\')"))

    return output


########################## show_note ##########################
# text = """
#       Please, try to show [job offer] note
#       show Morning Routine note
#       and don't forget to show note.
#       and don't forget to show all note.
#       Show       Note    [Hello]
#       """

def get_show_note(text):
    match = re.search(show_note_regex, text)
    output = []
    if match:
        matches = re.findall(show_note_regex, text)
        for match in matches:
            if match[1] == "all":
                pass
            else:
                output.append(("show_note", "title(\'" + match[1] + "\')"))

    another_regex = r"([Ss]how\s+[Nn]ote\s+(\[[\w ,_]*\]))"
    match = re.search(another_regex, text)
    if match:
        matches = re.findall(another_regex, text)
        for match in matches:
            output.append(("show_note", "title(\'" + match[1][1:-1] + "\')"))

    return output


########################## edit_note ##########################
# text = """
#       try to edit note [job offer] [You are totally rejected]
#       let's edit      note      [we are going to be OK [now, we are not], isA]
#       edit note [no]         [noo]
#       """

def get_edit_note(text):
    match = re.search(edit_note_regex, text)
    output = []
    if match:
        matches = re.findall(edit_note_regex, text)
        for match in matches:
            output.append(("edit_note", "title(\'" + match[1][1:-1] + "\')", \
                           "text(\'" + match[2][1:-1] + "\')"))

    return output


########################## delete_note ##########################
# text = """
#       try to delete note [job offer]
#       delete hey, YO Note
#       delete note
#       """

def get_delete_note(text):
    match = re.search(delete_note_regex, text)
    output = []
    if match:
        matches = re.findall(delete_note_regex, text)
        for match in matches:
            output.append(("delete_note", "title(\'" + match[1][1:-1] + "\')"))

    another_regex = show_note_regex = r"([Dd]elete\s+(.*)\s+[Nn]ote)"
    match = re.search(another_regex, text)
    if match:
        matches = re.findall(another_regex, text)
        for match in matches:
            output.append(("delete_note", "title(\'" + match[1] + "\')"))
    return output


# print get_delete_note(text), "\n\n\n"


########################## new_send ##########################
# text = """
#         send i've done with you to 011 27 55 70 54, please
#         send i've done with you to Mo7med 3adel, for God's sake
#         Send i've done with you to ismail@gmail.com, it's necessary
#         Send message to 011 [hello]
#         """

def get_new_send(text):
    output = []
    new_send_regex = r"([Ss]end\s+(.*)\s+to\s+(([A-Z0-9]\w*[\s\.]?)+))"
    match = re.search(new_send_regex, text)
    if match:
        matches = re.findall(new_send_regex, text)
        for match in matches:

            temp = delete_white_space(trim(match[2]))
            if trim(temp).isdigit() or match[1].lower() == "message":
                pass
            else:
                output.append(("message_contact", \
                               "contact_name(\'" + trim(match[2]) + "\')", \
                               "message(\'" + match[1] + "\')"))

    new_send_regex = r"([Ss]end\s+(.*)\s+to\s+([0-9\s-]{3,}))"
    match = re.search(new_send_regex, text)
    if match:
        matches = re.findall(new_send_regex, text)
        for match in matches:
            if match[1].lower() == "message":
                pass
            else:
                output.append(("message_number", \
                               "number(\'" + trim_number(match[2]) + "\')", \
                               "message(\'" + match[1] + "\')"))

    new_send_regex = r"([Ss]end\s+(.*)\s+to\s+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+))"
    match = re.search(new_send_regex, text)
    if match:
        matches = re.findall(new_send_regex, text)
        for match in matches:
            if match[1].lower() == "message":
                pass
            else:
                output.append(("send_email", \
                               "email(\'" + trim(match[2]) + "\')", \
                               "body(\'" + match[1] + "\')"))

    return output


#######################################################################




def extract_intents(text):
    whole_outputs = []
    whole_outputs.append(get_set_alarm(text))

    whole_outputs.append(get_call_number(text))
    whole_outputs.append(get_view_contact(text))
    whole_outputs.append(get_call_contact(text))

    whole_outputs.append(get_send_email(text))
    whole_outputs.append(get_new_send(text))

    whole_outputs.append(get_set_event(text))

    whole_outputs.append(get_message_contact(text))
    whole_outputs.append(get_message_number(text))

    whole_outputs.append(get_start_timer(text))

    whole_outputs.append(get_save_note(text))
    whole_outputs.append(get_edit_note(text))
    whole_outputs.append(get_show_note(text))
    whole_outputs.append(get_delete_note(text))

    if len(tuple(sum(whole_outputs, []))) == 0:
        return ("", "normal sentence")

    return ("intent", sum(whole_outputs, []))


# text = """
#       set alarm morning alarm 10:30 and please, call 011 27 55 70 54. View contact Mo7amed 3zzat call
#       M.Mostafa Elafasay. Try to send email to mohamed.anwar_vic@gmail.com [job offer] [You are totally rejected]
#       and send message to Amr 3zzat [How are you?]. Call 011
#
#       I'm in great mode, so let's know what is the day today and Save note [Great Moooode] [Yes].
#       And finally, show all notes out there :) Set alarm 10:00
#       set event 2017:8:14:17:32        [title] [description] [location]
#       show all notes. And in the last, Send i've done with you to ismail@gmail.com, it's necessary!!
#       ANd delete kza note
#       """
#
# print extract_intents(text)








