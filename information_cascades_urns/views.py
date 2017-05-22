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
        return self.round_number > 2 and self.round_number < Constants.num_rounds

    def vars_for_template(self):
<<<<<<< HEAD
        previous_players = [p for p
                            in self.subsession.get_players()
                            if p.choice_of_urn]

=======
>>>>>>> d5f5109e1be387a0e15953fb7708b6944d80da48
        return {
            #'total_performance': sum([p.payoff for p in self.player.in_all_rounds()]),
            'total_performance': self.player.payoff + Constants.endowment,
            'player_in_all_rounds': self.player.in_all_rounds(),
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
