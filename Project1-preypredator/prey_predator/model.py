"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed
import random

class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20
    initial_sheep = 100
    initial_wolves = 50
    sheep_reproduce = 0.04
    wolf_reproduce = 0.05
    wolf_gain_from_food = 20
    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    #Added parameters
    sheep_energy_loss_step=1
    wolf_energy_loss_step=1
    max_initial_wolf_energy=2
    max_initial_sheep_energy=2

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
        sheep_energy_loss_step=1,
        wolf_energy_loss_step=1,
        max_initial_wolf_energy=2,
        max_initial_sheep_energy=2
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.sheep_energy_loss_step=sheep_energy_loss_step
        self.wolf_energy_loss_step=wolf_energy_loss_step
        self.max_initial_wolf_energy=max_initial_wolf_energy
        self.max_initial_sheep_energy=max_initial_sheep_energy

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        # ... to be completed
        for i in range(self.initial_sheep):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            energy = random.randrange(self.max_initial_sheep_energy*self.sheep_gain_from_food)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.schedule.add(sheep)
            self.grid.place_agent(sheep, (x, y))

        # Create wolves
        # ... to be completed
        for i in range(self.initial_wolves):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            energy = random.randrange(self.max_initial_wolf_energy*self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.schedule.add(wolf)
            self.grid.place_agent(wolf, (x, y))

        # Create grass patches
        # ... to be completed
        for agent, x, y in self.grid.coord_iter():
            fully_grown = random.choice([True, False])
            if fully_grown:
                countdown = self.grass_regrowth_time
            else:
                countdown = random.randrange(self.grass_regrowth_time)
            patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)


        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

    def run_model(self, step_count=200):

        # ... to be completed
        for i in range(step_count):
            self.step()

