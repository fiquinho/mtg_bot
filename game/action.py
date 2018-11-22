from game.card import Card


class Action(object):

    def __init__(self):
        pass


class LandSpell(Action):

    def __init__(self, land_card: Card):
        Action.__init__(self)
        self.land_card = land_card


def create_action_by_card_type(card: Card):
    action = None

    if card.type == "land":
        action = LandSpell(land_card=card)

    if action is None:
        raise ValueError("Error with card type {}".format(card.type))
    return action
