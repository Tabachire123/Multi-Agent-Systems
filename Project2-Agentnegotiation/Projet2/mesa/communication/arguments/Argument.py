#!/usr/bin/env python3

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue

from communication.preferences.Value import Value

class Argument:
    """Argument class.
    This class implements an argument used in the negotiation.

    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__(self, boolean_decision, item):
        """Creates a new Argument.
        """
        self.__decision = boolean_decision
        self.__item = item
        self.__comparison_list = []
        self.__couple_values_list = []
        self.__premisses = []


    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self.__comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list.
        """
        self.__couple_values_list.append(CoupleValue(criterion_name, value))

    def __repr__(self):
        return f'{"" if self.__decision else "not"} {self.__item.get_name()} {(", ").join([str(couple) for couple in self.__couple_values_list])} \
{(", ").join([str(comp) for comp in self.__comparison_list])}'

    def list_supporting_proposal(self, item, preferences):
        """Generate a list of premisses which can be used to support an item
        :param item: Item - name of the item
        :param preferences: Preferences - preferences of the agent
        :return: list of all premisses PRO an item (sorted by order of importance based on agent's preferences)
        """
        supporting_proposal = []
        for criterion in preferences.get_criterion_name_list():
            if preferences.get_value(item, criterion) in [Value.GOOD, Value.VERY_GOOD]:
                supporting_proposal.append(criterion)
        return supporting_proposal

    def list_attacking_proposal(self, item, preferences):
        """Generate a list of premisses which can be used to attack an item
        :param item: Item - name of the item
        :param preferences: Preferences - preferences of the agent
        :return: list of all premisses CON an item (sorted by order of importance based on preferences)
        """
        attacking_proposal = []
        for criterion in preferences.get_criterion_name_list():
            if preferences.get_value(item, criterion) in [Value.BAD, Value.VERY_BAD]:
                attacking_proposal.append(criterion)
        return attacking_proposal

    def argument_parsing(self):
        """ returns ....
        :param argument:
        :return:
        """
        criterions = [(couple.get_criterion_name(),couple.get_value()) for couple in self.__couple_values_list]
        return criterions

    def get_decision(self):
        """Returns the decision of the argument.
        """
        return self.__decision

    def get_item(self):
        """Returns the item of the argument.
        """
        return self.__item



