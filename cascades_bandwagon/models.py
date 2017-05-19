from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Robin Engelhardt'
doc = """
Information Cascades with Bandwagon Effect
"""

class Constants(BaseConstants):
    name_in_url = 'cascades_bandwagon'
    players_per_group = None
    num_rounds = 7
    win = c(0.10)
    loose = c(-0.10)
    dunno = c(0)
    instructions_template = 'cascades_bandwagon/Instructions.html'
    urn_A = ['red', 'red', 'blue', 'black']
    urn_B = ['red', 'blue', 'blue', 'black']
    urns = ['A', 'B']


class Subsession(BaseSubsession):
    def before_session_starts(self):
        self.group_randomly()
        print(self.get_group_matrix())

        # make treatment groups with different storylines (e.g. different urns)
        # this works only if there are no group, e.g. Constants.num_rounds = None
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['storyline'] = random.choice(Constants.urns) # fix urn for all rounds

        for p in self.get_players():
            p.storyline = p.participant.vars['storyline']      # retrieve fixed urn for all rounds

        # let players draw a random ball in each round
        for p in self.get_players():
            if p.storyline == 'A':
                p.current_ball = random.choice(Constants.urn_A)
            else:
                p.current_ball = random.choice(Constants.urn_B)

        # make automatic bayesian rational choices in the first two rounds:
        if self.round_number == 1 or self.round_number == 2:
            for p in self.get_players():
                if p.current_ball == 'red':
                    p.choice_of_urn = 'A'
                elif p.current_ball == 'blue':
                    p.choice_of_urn = 'B'
                else:
                    if self.round_number == 1:
                        p.choice_of_urn = 'I don\'t know'
                    else:
                        p.choice_of_urn = p.in_round(
                            self.round_number - 1).choice_of_urn  # choose same as previous round


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    current_ball = models.CharField() # the color of the ball a player will draw
    choice_of_urn = models.CharField( # the guess by the player
        choices=['A', 'B', 'I don\'t know'],
        widget=widgets.RadioSelectHorizontal()
    )
    storyline = models.CharField() # for making treatment groups

    def set_payoffs(self):
        if self.choice_of_urn == self.storyline:
            self.payoff = Constants.win
        elif self.choice_of_urn == 'I don\'t know':
            self.payoff = Constants.dunno
        else:
            self.payoff = Constants.loose

