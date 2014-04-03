from pyramid.view import view_config, view_defaults

from .game import game, cards_for_phase
from .cards import Cards
from .utils import card_image_name


@view_defaults(renderer='templates/table.pt')
class TableView:

    def __init__(self, request):
        self.request = request

    def card_image_name(self, card):
        color, value = card
        return '{0}{1}.png'.format(value.upper(), color.upper())

    def show_cards(self, phase):
        return cards_for_phase.get(phase)

    def get_results(self):
        return sorted(
            game.players, 
            key=lambda player: player.account, 
            reverse=True
        )

    @view_config(route_name='home')
    def display_table(self):
        game.play()
        return {
            'table': game.cards,
            'players': game.players,
            'phase': game.phase,
            'pot': game.pot,
            'distribution': game.distribution,
            'actual_player': game.actual_player,
            'bet': game.bet,
        }
