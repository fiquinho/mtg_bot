import logging

from game.card import Card
from game.player import Player


logger = logging.getLogger()


class Action(object):

    def __init__(self, player: Player):
        self.player = player

    def __str__(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError


class NullAction(Action):
    def __init__(self, player: Player):
        Action.__init__(self, player=player)

    def __str__(self):
        return "Pass"

    def execute(self):
        return None


class DeployLand(Action):

    def __init__(self, player: Player, land_card: Card):
        Action.__init__(self, player=player)
        self.land_card = land_card

    def __str__(self):
        return "Place land on the board"

    def execute(self):
        assert self.land_card in self.player.hand
        self.land_card.location = "lands"
        self.player.lands.append(self.land_card)
        self.player.hand.remove(self.land_card)
        self.player.land_spells -= 1
        logger.info("{} - Played {}".format(self.player.name, self.land_card.name))

        return "ok"


class DeployCreature(Action):

    def __init__(self, player: Player, card: Card):
        Action.__init__(self, player=player)
        self.card = card

    def __str__(self):
        return "Place creature on the board"

    def execute(self):
        assert self.card in self.player.hand
        self.card.location = "creatures"
        self.player.creatures.append(self.card)
        self.player.hand.remove(self.card)
        logger.info("{} - Played {}".format(self.player.name, self.card.name))

        return "ok"


class AddBasicMana(Action):
    def __init__(self, player: Player):
        Action.__init__(self, player=player)

    def __str__(self):
        return "Add 1 basic mana to your mana pool"

    def execute(self):
        self.player.mana_pool += 1
        logger.info("{} - Added 1 basic mana to mana pool".format(self.player.name))

        return "ok"


def create_action_by_name(player: Player, name: str, card: Card=None) -> Action:
    if name == "add_mana_basic":
        action = AddBasicMana(player=player)

    elif name == "deploy_creature":
        if card is None:
            raise ValueError("Can't create action DeployCreature with card = None")
        action = DeployCreature(player=player, card=card)

    elif name == "deploy_land":
        if card is None:
            raise ValueError("Can't create action DeployLand with card = None")
        action = DeployLand(player=player, land_card=card)

    else:
        raise ValueError("Action name {} unknown.".format(name))

    return action
