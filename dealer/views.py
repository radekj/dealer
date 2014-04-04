from pyramid.view import view_config, view_defaults

from .game import game, cards_for_phase
from .cards import Cards
from .utils import card_image_name
from . import config


@view_defaults(renderer='templates/table.pt')
class TableView:

    def __init__(self, request):
        self.request = request

    def card_image_name(self, card):
        color, value = card
        return '{0}{1}.png'.format(value.upper(), color.upper())

    @view_config(route_name='home')
    def display_table(self):
        game.play()
        winners = [player for player in game.players if player.winner]
        return {
            'table': game.cards,
            'players': game.players,
            'phase': game.phase,
            'pot': game.pot,
            'distribution': game.distribution,
            'actual_player': game.actual_player,
            'bet': max(player.total_bet() for player in game.players),
            'winner': winners[0].name if winners else None,
            'table_cards': cards_for_phase.get(game.phase),
            'show_hand_cards': config.SHOW_HAND_CARDS,
            'results': sorted(
                game.players,
                key=lambda player: player.account,
                reverse=True,
            )
        }
