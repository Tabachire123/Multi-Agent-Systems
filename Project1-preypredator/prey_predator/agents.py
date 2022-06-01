from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        # ... to be completed
        self.energy -= self.model.sheep_energy_loss_step #reduce energy by one from moving
        if self.model.grass: #If grass eating is enabled
            #check if there is grass on the cell
            cell_content=self.model.grid.get_cell_list_contents([self.pos])
            grass=[content for content in cell_content if type(content)==GrassPatch]
            if grass[0].fully_grown:
                self.energy+=self.model.sheep_gain_from_food
                grass[0].fully_grown = False

        #if energy is too low we die
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.sheep_reproduce:
                # if the sheep is still alive it reproduces with the proba sheep_reproduce
                self.energy = int(self.energy / 2)
                new_sheep = Sheep(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(new_sheep, self.pos)
                self.model.schedule.add(new_sheep)

class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # ... to be completed
        self.energy -= self.model.wolf_energy_loss_step
        #check if there is a sheep on the cell
        cell_content=self.model.grid.get_cell_list_contents([self.pos])
        sheeps=[content for content in cell_content if type(content)==Sheep]
        if len(sheeps)!=0:
            #pick a random sheep to eat
            sheep=random.choice(sheeps)
            self.energy += self.model.wolf_gain_from_food
            # delete the sheep eaten
            self.model.grid._remove_agent(self.pos, sheep)
            self.model.schedule.remove(sheep)
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # if the wolf is still alive it reproduces with the proba sheep_reproduce
                self.energy = int(self.energy / 2)
                wolfie = Wolf(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(wolfie, self.pos)
                self.model.schedule.add(wolfie)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # ... to be completed
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        # ... to be completed
        if not self.fully_grown:
            if self.countdown <= 0:
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
