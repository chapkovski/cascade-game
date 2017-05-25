from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Subsession
import json
from channels.asgi import get_channel_layer
from .consumers import get_group_name
import channels


class WaitingRoom(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1 and self.subsession.room_busy


class Choose(Page):
    form_model = models.Player          # setting a form model for current player
    form_fields = ['choice_of_urn']     # setting a form field to fill out

    def is_displayed(self):
        self.subsession.room_busy = True
        self.subsession.save()
        return True

    def vars_for_template(self):
        previous_players = [p for p
                            in self.subsession.get_players()
                            if p.choice_of_urn]

        previous_players.sort(key=lambda x: x.decision_order, reverse=False)

        return {
            'previous_players': previous_players,
            'num_in_line': len(previous_players)+1
        }

    def before_next_page(self):
        self.subsession.room_busy = False
        self.subsession.save()
        channel_name =  get_group_name(self.subsession.pk, 1)
        channel_layer = get_channel_layer()
        ch_group_list = channel_layer.group_channels(channel_name)
        if len(ch_group_list) > 0:
            curchname = next(iter(ch_group_list.keys()))
            mychannel = channels.Channel(curchname)
            mychannel.send( {'text': json.dumps(
                    {'status': 'ready'})}
                    )


        self.player.decision_order = len([p for p
                                          in self.subsession.get_players()
                                          if p.choice_of_urn])

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    def is_displayed(self):
        self.player.set_payoffs()
        return True

    def vars_for_template(self):
        previous_players = [p for p
                            in self.subsession.get_players()
                            if p.choice_of_urn]

        previous_players.sort(key=lambda x: x.decision_order, reverse=False)
        return {
            'total_performance': self.player.payoff + Constants.endowment,
            'previous_players': previous_players,
        }

page_sequence = [
    WaitingRoom,
    Choose,
    Results,
]
