from model import *
from agent import BuildingAgent, CarAgent, TrafficLightAgent
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
    elif type(agent) is TrafficLightAgent:
        portrayal["Color"] = agent.colors[agent.state]
        portrayal["Layer"] = 1

    # elif type(agent) is CarAgent:
    #     if agent.velocity == (0, 1):
    #         portrayal["Color"] = "green"
    #     elif agent.velocity == (1, 0):
    #         portrayal["Color"] = "black"
    #     elif agent.velocity == (0, -1):
    #         portrayal["Color"] = "magenta"
    
    return portrayal


grid = CanvasGrid(agent_portrayal, total_width, total_height, 4 * total_width+1, 4 * total_height+1)
server = ModularServer(CityModel,
                       [grid],
                       "City Model")

server.launch()
