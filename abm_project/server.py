from model import *
from agent import BuildingAgent, CarAgent, TrafficLightAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "w": 0.5,
                 "h": 0.5}
    if isinstance(agent, BuildingAgent):
        portrayal["Color"] = "blue"
    if isinstance(agent, TrafficLightAgent):
        portrayal["Color"] = agent.colors[agent.state]
        portrayal["Layer"] = 1
        portrayal["w"] = 0.25
        portrayal["h"] = 0.25
    return portrayal


grid = CanvasGrid(agent_portrayal, total_width, total_height, 4 * total_width+1, 4 * total_height+1)
server = ModularServer(CityModel,
                       [grid],
                       "City Model")
