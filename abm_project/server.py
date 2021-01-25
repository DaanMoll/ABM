from mesa.visualization.UserParam import UserSettableParameter

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


max_car_agents = UserSettableParameter('slider', "Maximum number of Cars", 100, 10, 500, 1)
cars_per_second = UserSettableParameter('slider', "Number of new Cars per second", 5, 0, 16, 1)
tl_green_duration = UserSettableParameter('slider', "Traffic Light green/red duration", 5, 1, 20, 1)

grid = CanvasGrid(agent_portrayal, total_width, total_height, n_roads_horizontal * total_width+1, n_roads_vertical * total_height+1)
server = ModularServer(CityModel, [grid], "City Model",
                       {  # UI Input params
                           'max_car_agents': max_car_agents,
                           'cars_per_second': cars_per_second,
                           'tl_green_duration': tl_green_duration
                        })
