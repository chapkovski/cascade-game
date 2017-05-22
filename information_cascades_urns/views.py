from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Choose(Page):
    form_model = models.Player          # setting a form model for current player
    form_fields = ['choice_of_urn']     # setting a form field to fill out

    def vars_for_template(self):
        previous_players = [p for p
                            in self.subsession.get_players()
                            if p.choice_of_urn]
        self.subsession.n_done = len(previous_players)

        return {
            'previous_players': previous_players,
            'cur_num': self.subsession.n_done + 1
        }

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
        return {
            'total_performance': self.player.payoff + Constants.endowment,
            'player_in_all_rounds': previous_players,
        }

page_sequence = [
    Choose,
    Results,
]
