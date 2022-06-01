from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        # ... to be completed
        portrayal["Shape"] = "prey_predator/sheep.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1


    elif type(agent) is Wolf:
        # ... to be completed
        portrayal["Shape"] = "prey_predator/wolf.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    elif type(agent) is GrassPatch:
        # ... to be completed
        if agent.fully_grown:
            portrayal["Color"] = ["#004C00"]
        else:
            portrayal["Color"] = ["#CCDBCC"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    # ... to be completed

    "grass": UserSettableParameter("checkbox", "Grass Enabled", True),
    "grass_regrowth_time": UserSettableParameter(
        "slider", "Grass Regrowth Time", 30, 1, 100
    ),
    "initial_sheep": UserSettableParameter(
        "slider", "Initial Sheep Population", 100, 10, 300
    ),
    "initial_wolves": UserSettableParameter(
        "slider", "Initial Wolf Population", 50, 10, 300
    ),
    "wolf_reproduce": UserSettableParameter(
        "slider",
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
    ),
    "sheep_reproduce": UserSettableParameter(
        "slider", "Sheep Reproduction", 0.04, 0.01, 1.0, 0.01
    ),
    "wolf_gain_from_food": UserSettableParameter(
        "slider", "Wolf Gain From Food", 20, 1, 50
    ),
    "sheep_gain_from_food": UserSettableParameter(
        "slider", "Sheep Gain From Food", 4, 1, 10
    ),
    "sheep_energy_loss_step": UserSettableParameter(
        "slider", "Sheep Energy Loss", 1, 1, 10),
    "wolf_energy_loss_step": UserSettableParameter(
        "slider", "Wolf Energy Loss", 1, 1, 10),
    "max_initial_wolf_energy": UserSettableParameter(
        "slider", "Initial Energy Multiplier Wolf", 1, 1, 10),
        "max_initial_sheep_energy": UserSettableParameter(
        "slider", "Initial Energy Multiplier Sheep", 1, 1, 10),
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
