from typing import List

from game.player import Player
from game.card import Card


class AbilityCosts(object):
    def __init__(self, costs: List):
        self.raw_costs = costs
        self.costs = []

        for cost in costs:
            cost_instance = create_cost_instance(cost)
            self.costs.append(cost_instance)

    def __str__(self):
        return str(self.raw_costs)

    def check_costs(self, player: Player, card: Card):
        for cost in self.costs:
            cost_check = cost.check_cost(player=player, card=card)
            if not cost_check:
                return False

        return True

    def pay_costs(self, player: Player, card: Card):

        for cost in self.costs:
            cost.pay_cost(player=player, card=card)


class BaseCost(object):
    def pay_cost(self, player: Player, card: Card):
        raise NotImplementedError

    def check_cost(self, player: Player, card: Card):
        raise NotImplementedError


class NoneCost(BaseCost):
    def __init__(self):
        pass

    def check_cost(self, player: Player, card: Card):
        pass

    def pay_cost(self, player: Player, card: Card):
        pass


class ManaCost(BaseCost):
    def __init__(self, mana_cost):
        self.mana_cost = mana_cost

    def check_cost(self, player: Player, card: Card):
        return player.mana_pool >= self.mana_cost

    def pay_cost(self, player: Player, card: Card):
        player.mana_pool -= self.mana_cost


class TapCard(BaseCost):
    def __init__(self):
        pass

    def check_cost(self, player: Player, card: Card):
        return card.status == "ready"

    def pay_cost(self, player: Player, card: Card):
        card.status = "tapped"


class LandSpell(BaseCost):
    def __init__(self):
        pass

    def check_cost(self, player: Player, card: Card):
        return player.land_spells >= 1

    def pay_cost(self, player: Player, card: Card):
        player.land_spells -= 1


class CardReady(BaseCost):
    def __init__(self):
        pass

    def check_cost(self, player: Player, card: Card):
        return card.status == "ready"

    def pay_cost(self, player: Player, card: Card):
        pass


def create_cost_instance(cost) -> BaseCost:
    if cost is None:
        cost_instance = NoneCost()
    elif type(cost) == int:
        cost_instance = ManaCost(cost)
    elif cost == "tap_this":
        cost_instance = TapCard()
    elif cost == "land_spell":
        cost_instance = LandSpell()
    elif cost == "ready":
        cost_instance = CardReady()
    else:
        raise ValueError("{} mana cost unknown".format(cost))

    return cost_instance
