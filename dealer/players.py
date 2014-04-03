import random

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from dealer.connector import connector
from dealer import config, utils


class Player:

    def __init__(self, player_id, player_data):
        self.player_id = player_id
        self.active = True
        self.hand = []
        self.account = player_data['account']
        self.name = player_data['name']
        self.address = player_data['address']
        self.deal_bet = 0
        self.winner = False

    def new_distribution(self):
        self.hand = []
        self.active = self.account > 0
        self.deal_bet = 0
        self.winner = False

    def bet(self, data):
        player_bet = connector.ask_for_decision(self.address, data)
        return player_bet

    def hand_value(self, table):
        hand = [Card(*card) for card in utils.card_values(self.hand)]
        table = [Card(*card) for card in utils.card_values(table)]
        score = HandEvaluator.evaluate_hand(hand, table)
        return score
