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

        previous_players.sort(key=lambda x: x.decision_order, reverse=False)

        return {
            'previous_players': previous_players,
            'num_in_line': len(previous_players)+1
        }

    def before_next_page(self):
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
    Choose,
    Results,
]
