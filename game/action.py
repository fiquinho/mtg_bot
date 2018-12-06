import logging

from game.card import Card, CreatureCard
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
        logger.info("{} - Passed".format(self.player.name))
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


class PlayerAttack(Action):
    def __init__(self, player: Player):
        Action.__init__(self, player=player)

    def __str__(self):
        return "Attack with selected creatures"

    def execute(self):
        return "attack"


class CreatureAttack(Action):
    def __init__(self, player: Player, card: Card):
        Action.__init__(self, player=player)
        self.card = card

    def __str__(self):
        return "Attack with creature"

    def execute(self):
        self.player.attacking_creatures.append(self.card)
        logger.info("{} - Added {} to attacking creatures".format(self.player.name,
                                                                  self.card.name))

        return "ok"


class CreatureBlock(Action):
    def __init__(self, player: Player, card: Card, attacking_player: Player):
        Action.__init__(self, player=player)
        self.card = card
        self.attacking_player = attacking_player

    def __str__(self):
        return "Block with creature"

    def execute(self):
        self.player.blocking_creatures.append(self.card)
        logger.info("{} please select creature to block: ".format(self.attacking_player.name))
        for i, attack_creature in enumerate(self.attacking_player.attacking_creatures):
            logger.info("   {} - {} - {}/{}".format(i, attack_creature.name,
                                                    attack_creature.attack, attack_creature.defense))

        selection = int(input("{} please select creature to block: ".format(self.attacking_player.name)))

        blocked_creature = self.attacking_player.attacking_creatures[selection - 1]
        blocked_creature.blocking_creatures.append(blocked_creature)
        self.card.saved_status = self.card.status
        self.card.status = "blocking"

        return "ok"


def create_action_by_name(player: Player, name: str, card: Card=None,
                          opponent: Player=None) -> Action:
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

    elif name == "attack":
        if card is None:
            raise ValueError("Can't create action Attack with card = None")
        action = CreatureAttack(player=player, card=card)

    elif name == "block":
        if card is None:
            raise ValueError("Can't create action Block with card = None")
        action = CreatureBlock(player=player, card=card, attacking_player=opponent)

    else:
        raise ValueError("Action name {} unknown.".format(name))

    return action
