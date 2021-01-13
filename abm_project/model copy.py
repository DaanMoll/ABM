from mesa import Model
from mesa.space import SingleGrid
from mesa.time import BaseScheduler
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from agent import CarAgent, BuildingAgent

import random

n_roads_horizontal = 4
n_roads_vertical = 4

road_width = 2

distance_roads_hortizontal = 20
distance_roads_vertical = 20


class CityModel(Model):
    def __init__(self):
        super().__init__()
        self.unique_id = 0
        # self.number_of_agents = N
        self.agents = []

        self.grid = SingleGrid(width=distance_roads_hortizontal * (n_roads_horizontal+1) + n_roads_horizontal * road_width,
                               height=distance_roads_vertical * (n_roads_vertical+1) + n_roads_vertical * road_width,
                               torus=False)

        road_pos = self.create_buildings()
        self.create_agents(road_pos[1], road_pos[2])

    def get_new_unique_id(self):
        self.unique_id += 1
        return self.unique_id

    def create_buildings(self):
        """
        Populates area between roads with buildings.
        """
        road_pos_x = [distance_roads_hortizontal * i + 1 for i in range(1, n_roads_horizontal + 1)] + \
                     [distance_roads_hortizontal * i + 2 for i in range(1, n_roads_horizontal + 1)]         
        road_pos_y = [distance_roads_vertical * i + 1 for i in range(1, n_roads_vertical + 1)] + \
                     [distance_roads_vertical * i + 2 for i in range(1, n_roads_vertical + 1)]
        road_pos = set(road_pos_x + road_pos_y)
    
        for x, y in self.grid.empties.copy():
            if not (x in road_pos or y in road_pos):  # not a road -> building
                building = BuildingAgent(unique_id=self.get_new_unique_id(), pos=(x, y))
                self.grid.place_agent(building, pos=(x, y))
        
        intersections = set((x, y) for x in road_pos_x for y in road_pos_y)
        self.intersections = intersections

        return road_pos, road_pos_x, road_pos_y

    def create_agents(self, road_pos_x, road_pos_y):
        starting_points_top = [(x, self.grid.height-1) for x in road_pos_x if x%2!=0]
        starting_points_bottom = [(x, 0) for x in road_pos_x if x%2==0]
        
        starting_points_left = [(0, y) for y in road_pos_y if y%2!=0]
        starting_points_right = [(self.grid.width-1, y) for y in road_pos_y if y%2==0]

        starting_points = starting_points_top + starting_points_bottom + starting_points_left + starting_points_right

        end_points_top = [(x, self.grid.height-1) for x in road_pos_x if x%2==0]
        end_points_bottom = [(x, 0) for x in road_pos_x if x%2!=0]

        end_points_left = [(0, y) for y in road_pos_y if y%2==0]
        end_points_right = [(self.grid.width-1, y) for y in road_pos_y if y%2!=0]

        end_points = end_points_top + end_points_bottom + end_points_left + end_points_right

        for start_point in starting_points:
            if start_point[0] == 0:
                velocity_vector = (1, 0)
            elif start_point[0] == self.grid.height-1:
                velocity_vector = (-1, 0)
            elif start_point[1] == 0:
                velocity_vector = (0, 1)
            else:
                velocity_vector = (0, -1)

            end_point = random.choice(end_points)

            agent = CarAgent(unique_id=self.get_new_unique_id(), model=self, pos=start_point, velocity=1, velocity_vector=velocity_vector, destination=end_point)
            self.grid.place_agent(agent, pos=start_point)
            self.agents.append(agent)
            break
            
    def step(self):
        '''
        Method that steps every agent. 
        
        Prevents applying step on new agents by creating a local list.
        '''
        for agent in list(self.agents):
            agent.step()
            

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 1}

    if type(agent) == BuildingAgent:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    elif type(agent) == CarAgent:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 1
    return portrayal

if __name__ == '__main__':
    model = CityModel()
    model.step()

    grid = CanvasGrid(agent_portrayal, 100, 108, 540, 540)
    server = ModularServer(CityModel,
                        [grid],
                        "City Model")
    server.port = 8521 # The default
    server.launch()