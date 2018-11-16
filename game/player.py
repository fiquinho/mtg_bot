from game.deck import Deck


class Player(object):

    def __init__(self, deck: Deck, hp: int):

        self.deck = deck
        self.hand = []
        self.health_points = hp

    def draw_card(self, cards_count: int=1):
        for i in range(cards_count):
            draw_card = self.deck.draw_card()
            self.hand.append(draw_card)
