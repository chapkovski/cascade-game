from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Choose(Page):
    # def is_displayed(self):
    #     return self.round_number > 2    # only shown after round 2

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
    # def is_displayed(self):
    #     self.player.set_payoffs()
    #     return self.round_number > 2 and self.round_number < Constants.num_rounds

    def vars_for_template(self):
        previous_players = [p for p
                            in self.subsession.get_players()
                            if p.choice_of_urn]
        return {
            #'total_performance': sum([p.payoff for p in self.player.in_all_rounds()]),
            'total_performance': self.player.payoff + Constants.endowment,
            'player_in_all_rounds': previous_players,
        }

class FinalResults(Page):
    def is_displayed(self):
        self.player.set_payoffs()
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'total_performance': sum(
                [p.payoff for p in self.player.in_all_rounds()]),
            'player_in_all_rounds': self.player.in_all_rounds(),
        }


page_sequence = [
    #Introduction,
    Choose,
    Results,
    #FinalResults
]
