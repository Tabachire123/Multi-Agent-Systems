from mesa import Model
from mesa.time import RandomActivation
import numpy as np
import random

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService

from communication.preferences.Item import Item
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService

from communication.arguments.Argument import Argument
from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue

nb_item=2
mode='sujet'

class ArgumentAgent(CommunicatingAgent):
    """ TestAgent which inherit from CommunicatingAgent.
    """
    def __init__(self, unique_id, model, name,list_items):
        super().__init__(unique_id, model, name)
        self.preference = None
        self.commit = False
        self._arguments=[]
        self._list_items = list_items
        self._list_items_left=list_items.copy()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, list_items):
        self.preference=Preferences()
        criterions=[CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE]
        np.random.shuffle(criterions)
        self.preference.set_criterion_name_list(criterions)
        for item in list_items:
            values=[Value.VERY_GOOD,Value.GOOD,Value.AVERAGE,
                               Value.BAD,Value.VERY_BAD]
            np.random.shuffle([Value.VERY_GOOD,Value.GOOD,Value.AVERAGE,
                               Value.BAD,Value.VERY_BAD])

            self.preference.add_criterion_value(CriterionValue(item, CriterionName.PRODUCTION_COST,
                                                  values[0]))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.CONSUMPTION,
                                                          values[1]))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.DURABILITY,
                                                          values[2]))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT,
                                                          values[3]))
            self.preference.add_criterion_value(CriterionValue(item, CriterionName.NOISE,
                                                          values[4]))

    def generate_sujet(self,list_items,list_criteres,num_agent):
        self.preference=Preferences()

        self.preference.set_criterion_name_list(list_criteres)
        if num_agent==1:
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.PRODUCTION_COST,Value.VERY_GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.CONSUMPTION,Value.GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.DURABILITY,Value.VERY_GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.ENVIRONMENT_IMPACT,Value.VERY_BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.NOISE,Value.BAD))

            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.PRODUCTION_COST,Value.BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.CONSUMPTION,Value.VERY_BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.DURABILITY,Value.GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.ENVIRONMENT_IMPACT,Value.VERY_GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.NOISE,Value.VERY_GOOD))
        if num_agent==2:
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.PRODUCTION_COST,Value.GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.CONSUMPTION,Value.BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.DURABILITY,Value.GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.ENVIRONMENT_IMPACT,Value.VERY_BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[0], CriterionName.NOISE,Value.VERY_BAD))

            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.PRODUCTION_COST,Value.GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.CONSUMPTION,Value.BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.DURABILITY,Value.BAD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.ENVIRONMENT_IMPACT,Value.VERY_GOOD))
            self.preference.add_criterion_value(CriterionValue(list_items[1], CriterionName.NOISE,Value.VERY_GOOD))

    def step(self):
        super().step()
        list_messages=self.get_new_messages()

        for message in list_messages:
            print(message)

            if message.get_performative() == MessagePerformative.PROPOSE:
                item = message.get_content()
                sender=message.get_exp()
                if self.preference.is_item_among_top_10_percent(item,self.model.list_items):
                    self.send_message(Message(from_agent=self.get_name(),
                                              to_agent=sender,
                                              message_performative=MessagePerformative.ACCEPT,
                                              content=item))
                else:
                    self.send_message(Message(from_agent=self.get_name(),
                                              to_agent=sender,
                                              message_performative=MessagePerformative.ASK_WHY,
                                              content=item))
            if message.get_performative() == MessagePerformative.ACCEPT or message.get_performative() == MessagePerformative.COMMIT:
                if not self.commit:
                    self.commit=True
                    sender=message.get_exp()
                    self.send_message(Message(from_agent=self.get_name(),
                                              to_agent=sender,
                                              message_performative=MessagePerformative.COMMIT,
                                              content=message.get_content()))

            if message.get_performative() == MessagePerformative.ASK_WHY:
                sender=message.get_exp()
                item = message.get_content()
                arg_to_send= self.support_proposal(item)
                self.send_message(Message(from_agent=self.get_name(),
                                          to_agent=sender,
                                          message_performative=MessagePerformative.ARGUE,
                                          content=arg_to_send)
                )

            if message.get_performative() == MessagePerformative.ARGUE:
                argument = message.get_content()
                item=argument.get_item()
                attack_argument = self.attackable(argument)
                if attack_argument:
                    if self.counter_argument(argument) is not None:
                        self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content=self.counter_argument(argument)))
                    else:
                        self._list_items_left.remove(item)
                        self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=random.choice(self._list_items_left)))


    def support_proposal(self, item):
        """
        Used when the agent receives "ASK_WHY" after having proposed an item
        :param item: str - name of the item which was proposed
        :return string - the strongest supportive argument
        """
        arg = Argument(boolean_decision=True, item=item)
        possible_proposals = arg.list_supporting_proposal(
            item, self.preference)
        final_arg = Argument(boolean_decision=True, item=item)
        value = self.preference.get_value(item, possible_proposals[0])
        final_arg.add_premiss_couple_values(possible_proposals[0],value)
        return final_arg


    def attackable(self,argument):
        proposed_item=argument.get_item()
        counter_argument = Argument(False, proposed_item)
        criterion=argument.argument_parsing()[0][0]
        value_criterion=argument.argument_parsing()[0][1]
        criterion_order=self.preference.get_criterion_name_list()

        #Another prefered criterion
        for other_criterions in criterion_order:
            if self.preference.is_preferred_criterion(other_criterions, criterion) and other_criterions!=criterion:
                counter_argument.add_premiss_comparison(criterion_name_1=other_criterions,
                                                        criterion_name_2=criterion)

                return True

        #Local value for the item lower than one of the other agent for the criteria

        if self.preference.get_value(proposed_item, criterion).value < value_criterion.value:
                    counter_argument.add_premiss_couple_values(criterion,self.preference.get_value(proposed_item, criterion))

                    return True

        #Other item with higher value on the same criterion:
        for item in self.model.list_items:
                    if self.preference.get_value(item, criterion).value > value_criterion.value:
                        other_arg = Argument(True, item)
                        possible_proposals = other_arg.list_supporting_proposal(
                                item, self.preference)
                        other_arg.add_premiss_couple_values(possible_proposals[0],self.preference.get_value(item, criterion))
                        return other_arg

        return False

    def counter_argument(self,argument):
        item=argument.get_item()
        preferences=self.preference
        possible_counter_arg=argument.list_attacking_proposal(item,preferences)
        criterion=argument.argument_parsing()[0][0]
        counter_arg=Argument(False, item)
        for arg in possible_counter_arg:
            if self.preference.is_preferred_criterion(arg,criterion) and arg!=criterion:
                counter_arg.add_premiss_couple_values(arg,self.preference.get_value(item,arg))
                counter_arg.add_premiss_comparison(arg,criterion)
                return counter_arg




class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        # To be completed
        if mode=='general':
            list_items=[Item(str(i),'item '+str(i)) for i in range(nb_item)]
            self.list_items=list_items
            a = ArgumentAgent(1, self, "Ismail",list_items)
            a.generate_preferences(list_items)
            self.schedule.add(a)
            # ...
            b = ArgumentAgent(2, self, "Ayoub",list_items)
            b.generate_preferences(list_items)
            self.schedule.add(b)

        else:
            diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
            electric_engine = Item("Electric Engine", "A very quiet and ecofriendly engine")
            list_items = [diesel_engine, electric_engine]
            self.list_items=list_items
            a = ArgumentAgent(1, self, "Ismail",list_items)
            list_criteres_a=[CriterionName.PRODUCTION_COST,CriterionName.ENVIRONMENT_IMPACT,
                             CriterionName.CONSUMPTION,CriterionName.DURABILITY,CriterionName.NOISE]
            a.generate_sujet(list_items,list_criteres_a,1)
            self.schedule.add(a)
            # ...
            list_criteres_b=[CriterionName.ENVIRONMENT_IMPACT,CriterionName.NOISE,CriterionName.PRODUCTION_COST,
                             CriterionName.CONSUMPTION,CriterionName.DURABILITY]
            b = ArgumentAgent(2, self, "Ayoub",list_items)
            b.generate_sujet(list_items,list_criteres_b,2)
            self.schedule.add(b)


        # Kick off the loop, the agent send his most preferred item

        most_preferred_item = a.preference.most_preferred(list_items)
        a.send_message(Message(a.get_name(), b.get_name(), MessagePerformative.PROPOSE, most_preferred_item))


        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()



if __name__ == "__main__":
    argument_model = ArgumentModel()

    for i in range(10):
        argument_model.step()
    # To be completed
