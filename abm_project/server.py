from model import *
from agent import BuildingAgent, CarAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "w": 0.5,
                 "h": 0.5}

    if type(agent) is BuildingAgent:
        portrayal["Color"] = "blue"

    return portrayal


grid = CanvasGrid(agent_portrayal, total_width, total_height, 4 * total_width+1, 4 * total_height+1)
server = ModularServer(CityModel,
                       [grid],
                       "City Model")

server.launch()
