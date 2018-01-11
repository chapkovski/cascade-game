from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Robin Engelhardt, Philipp Chapkovski'
doc = """
Information Cascades with urns
"""

class Constants(BaseConstants):
    name_in_url = 'information_cascades_urns'
    players_per_group = None
    num_rounds = 1
    bonus = c(0.10)
    endowment = c(0.10)
    instructions_template = 'information_cascades_urns/Instructions.html'
    urn_A = ['red', 'red', 'blue']
    urn_B = ['red', 'blue', 'blue']
    urns = ['A', 'B']
    # default values for pay_per_min and wait_before_leave
    pay_per_min = .1
    wait_before_leave = 30

class Subsession(BaseSubsession):
    storyline = models.CharField()
    room_busy = models.BooleanField(initial=False)
    pay_per_min = models.FloatField(doc='how much to pay per minute of waiting. Set to 0 to pay nothing')
    wait_before_leave = models.IntegerField(doc='how many seconds to wait. Set to negative number '
                                                'to switch off the option. Set to 0 to show immediately')

    def creating_session(self):
        self.storyline = random.choice(Constants.urns)
        self.pay_per_min = self.session.config.get('pay_per_min', Constants.pay_per_min)
        self.wait_before_leave = self.session.config.get('wait_before_leave', Constants.wait_before_leave)
        for p in self.get_players():
            if self.storyline == 'A':
                p.current_ball = random.choice(Constants.urn_A)
            else:
                p.current_ball = random.choice(Constants.urn_B)


class Group(BaseGroup):
    ...
from django.db import models as djmodels


class Player(BasePlayer):
    early_finish = models.BooleanField(doc='if decided to abandon the waiting page clickin Finish the study')
    wp_timer_start = djmodels.DateTimeField(null=True, blank=True)
    sec_spent = models.IntegerField(doc='number of seconds spent on waiting page')
    sec_earned = models.FloatField(doc='dollars earned for waiting')
    decision_order = models.IntegerField(initial=10^10)
    current_ball = models.CharField()                   # the color of the ball a player will draw
    choice_of_urn = models.CharField(                   # the guess by the player
        choices=['A', 'B'],
        widget=widgets.RadioSelectHorizontal()
    )

    def set_payoffs(self):
        if self.choice_of_urn == self.subsession.storyline:
            self.payoff = Constants.bonus
        else:
            self.payoff = 0
