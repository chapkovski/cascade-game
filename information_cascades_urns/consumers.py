from channels import Group
from channels.sessions import channel_session
import random
from .models import Player, Subsession, Constants
import json



def get_group_name(subsession_pk, index_in_pages):
    group_name = 'mturkchannel_{}_{}'.format(subsession_pk,
                                             index_in_pages,
                                             )
    return group_name



def ws_connect(message, subsession, index_in_pages):
    cursubsession = Subsession.objects.get(pk=subsession)
    print('somebody connected...')
    Group(get_group_name(subsession, index_in_pages)).add(message.reply_channel)


def ws_message(message):
    ...


# Connected to websocket.disconnect
def ws_disconnect(message, subsession, index_in_pages):
    print('somebody disconnected...')
    Group(get_group_name(subsession, index_in_pages)).discard(message.reply_channel)
