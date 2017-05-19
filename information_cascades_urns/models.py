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
    num_rounds = 20
    bonus = c(0.10)
    endowment = c(0.10)
    instructions_template = 'information_cascades_urns/Instructions.html'
    urn_A = ['red', 'red', 'blue']
    urn_B = ['red', 'blue', 'blue']
    urns = ['A', 'B']

class Subsession(BaseSubsession):
    def before_session_starts(self):
        # PS: see app cascades_bystander for an other solution with treatments creating one big group
        # the method below creates as many groups as there are participants, one participant in each group
        # by transposing the player matrix so that groups are ordered in columns
        if self.round_number == 1:
            matrix = [list(i) for i in zip(*self.get_group_matrix())]
            print(matrix)
            self.set_group_matrix(matrix)
            for g in self.get_groups():                         # different storylines for different groups
                p1 = g.get_player_by_id(1)
                p1.participant.vars['storyline'] = random.choice(Constants.urns) # save in participant vars
                print(p1.participant.vars)
        else:
            self.group_like_round(1)

        # retrieve storyline for each group from participant vars and find a ball for each player/group
        for g in self.get_groups():
            p1 = g.get_player_by_id(1)
            g.storyline = p1.participant.vars['storyline']
            if p1.participant.vars['storyline'] == 'A':
                p1.current_ball = random.choice(Constants.urn_A)
                if self.round_number == 1 or self.round_number == 2:    # generate first two player choices
                    if p1.current_ball == 'red':
                        p1.choice_of_urn = 'A'
                    else:
                        p1.choice_of_urn = 'B'
            else:
                p1.current_ball = random.choice(Constants.urn_B)
                if self.round_number == 1 or self.round_number == 2:    # generate first two player choices
                    if p1.current_ball == 'red':
                        p1.choice_of_urn = 'A'
                    else:
                        p1.choice_of_urn = 'B'

class Group(BaseGroup):
    storyline = models.CharField()

class Player(BasePlayer):
    current_ball = models.CharField()                   # the color of the ball a player will draw
    choice_of_urn = models.CharField(                   # the guess by the player
        choices=['A', 'B'],
        widget=widgets.RadioSelectHorizontal()
    )

    def set_payoffs(self):
        if self.choice_of_urn == self.group.storyline:
            self.payoff = Constants.bonus
        else:
            self.payoff = 0