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
                 "h": 0.5}
    if isinstance(agent, BuildingAgent):
        portrayal["Color"] = "darkgrey"
    if isinstance(agent, TrafficLightAgent):
        portrayal["Color"] = agent.colors[agent.state]
        portrayal["Layer"] = 1
        portrayal["w"] = 0.25
        portrayal["h"] = 0.25
    if isinstance(agent, CarAgent) and agent.haste == 1:
        portrayal["Color"] = "darkorange"
    if isinstance(agent, CarAgent) and agent.haste == 2:
        portrayal["Color"] = "darkred"
    if isinstance(agent, CarAgent) and agent.haste == 3:
        portrayal["Color"] = "purple"
    return portrayal


chart = ChartModule([
    {"Label": "AverageCongestion", "Color": "pink"},
    {"Label": "AverageSteps", "Color": "red"}], data_collector_name='datacollector', canvas_height=500, canvas_width=1000,)


grid = CanvasGrid(agent_portrayal, total_width, total_height, 4 * total_width+1, 4 * total_height+1)
server = ModularServer(CityModel,
                       [grid, chart],
                       "City Model")
