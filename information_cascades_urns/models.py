from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Robin Engelhardt'
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

class Subsession(BaseSubsession):
    storyline = models.CharField()
    room_busy = models.BooleanField(initial=False)

    def before_session_starts(self):
        self.storyline = random.choice(Constants.urns)
        for p in self.get_players():
            if self.storyline == 'A':
                p.current_ball = random.choice(Constants.urn_A)
            else:
                p.current_ball = random.choice(Constants.urn_B)


class Group(BaseGroup):
    ...

class Player(BasePlayer):
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
