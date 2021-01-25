from mesa.visualization.UserParam import UserSettableParameter

from model import *
from agent import BuildingAgent, CarAgent, TrafficLightAgent
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "w": 0.5,
                 "h": 0.5,
                 "r": 3}
    if isinstance(agent, BuildingAgent):
        portrayal["Color"] = "darkgrey"
    if isinstance(agent, TrafficLightAgent):
        portrayal["Color"] = agent.colors[agent.state]
        portrayal["Layer"] = 1
        portrayal["w"] = 0.25
        portrayal["h"] = 0.25
    if isinstance(agent, CarAgent) and agent.haste == 1:
        portrayal["Color"] = "darkorange"
    return portrayal


chart = ChartModule([
    {"Label": "AverageCongestion", "Color": "pink"},
    {"Label": "HastePercent", "Color": "red"}], data_collector_name='datacollector', canvas_height=500, canvas_width=1000,)

max_car_agents = UserSettableParameter('slider', "Maximum number of Cars", 100, 10, 500, 1)
cars_per_second = UserSettableParameter('slider', "Number of new Cars per second", 5, 0, 16, 1)
max_velocity = UserSettableParameter('slider', "Maximum allowed velocity", 5, 1, 10, 1)
green_light_duration = UserSettableParameter('slider', "Traffic Light green/red duration", 5, 1, 20, 1)

grid = CanvasGrid(agent_portrayal, total_width, total_height, n_roads_horizontal * total_width+1, n_roads_vertical * total_height+1)
server = ModularServer(CityModel, [grid, chart], "City Model",
                       {  # UI Input params
                           'max_car_agents': max_car_agents,
                           'cars_per_second': cars_per_second,
                           'green_light_duration': green_light_duration,
                           'max_velocity': max_velocity
                        })
