from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, Subsession
import json
from channels.asgi import get_channel_layer
from .consumers import get_group_name
import channels
from random import choice
import datetime


class WaitingRoom(Page):
    def dispatch(self, *args, **kwargs):
        super().dispatch(*args, **kwargs)
        if self.request.method == 'POST':
            end_of_game = self.request.POST.dict().get('endofgame')
            if end_of_game is not None:
                models.Player.objects.filter(pk=self.player.pk).update(early_finish=True)
        response = super().dispatch(*args, **kwargs)
        return response

    def record_secs_waited(self, p):
        self.pay_per_min = self.subsession.pay_per_min
        self.wait_before_leave = self.subsession.wait_before_leave
        p.sec_spent = (
            datetime.datetime.now(datetime.timezone.utc) - p.wp_timer_start).total_seconds()

        p.sec_earned = round(p.sec_spent / 60 * self.pay_per_min, 2)

    def is_displayed(self):
        if self.player.early_finish:
            return False
        if not self.player.wp_timer_start:
            self.player.wp_timer_start = datetime.datetime.now(datetime.timezone.utc)
        self.record_secs_waited(self.player)
        return self.subsession.room_busy

    def vars_for_template(self):
        return ({'index_in_pages': self._index_in_pages,
                 'time_left': max(self.wait_before_leave - self.player.sec_spent, 0)
                 })

    def before_next_page(self):
        self.record_secs_waited(self.player)


class Choose(Page):
    form_model = models.Player
    form_fields = ['choice_of_urn']

    # timeout_seconds = 20
    # timeout_submission = {'choice_of_urn': choice(['A', 'B'])}

    def is_displayed(self):
        self.subsession.room_busy = True
        self.subsession.save()
        return not self.player.early_finish

    def vars_for_template(self):
        previous_players = [p for p
                            in self.subsession.get_players()
                            if p.choice_of_urn]

        previous_players.sort(key=lambda x: x.decision_order, reverse=False)

        return {
            'previous_players': previous_players,
            'num_in_line': len(previous_players) + 1
        }

    def before_next_page(self):
        self.subsession.room_busy = False
        self.subsession.save()
        channel_name = get_group_name(self.subsession.pk, 1)
        channel_layer = get_channel_layer()
        ch_group_list = channel_layer.group_channels(channel_name)
        if len(ch_group_list) > 0:
            if isinstance(ch_group_list, list):
                curname = ch_group_list[0]
            elif isinstance(ch_group_list, dict):
                curname = next(iter(ch_group_list.keys()))
            else:
                return None

            mychannel = channels.Channel(curname)
            mychannel.send({'text': json.dumps(
                {'status': 'ready'})}
            )

        self.player.decision_order = len([p for p
                                          in self.subsession.get_players()
                                          if p.choice_of_urn])


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return not self.player.early_finish


class Results(Page):
    def is_displayed(self):
        self.player.set_payoffs()
        return not self.player.early_finish

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
