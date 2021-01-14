import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import BaseScheduler
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from agent import CarAgent, BuildingAgent, IntersectionAgent

import random

n_roads_horizontal = 4
n_roads_vertical = 4

road_width = 2

building_width = 20
building_height = 20

total_width = building_width * (n_roads_horizontal + 1) + n_roads_horizontal * road_width
total_height = building_height * (n_roads_vertical + 1) + n_roads_vertical * road_width


class CityModel(Model):
    def __init__(self):
        super().__init__()
        self.unique_id = 0
        # self.number_of_agents = N
        self.agents = []

        self.grid = SingleGrid(width=total_width, height=total_height, torus=False)

        road_pos = self.create_buildings()
        self.create_agents(road_pos[1], road_pos[2])

    def get_new_unique_id(self):
        self.unique_id += 1
        return self.unique_id

    def create_buildings(self):
        """
        Populates area between roads with buildings.
        """
        road_pos_x = [building_width * i + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)] + \
                     [building_width * i + 1 + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)]
        road_pos_y = [building_height * i + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)] + \
                     [building_height * i + 1 + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)]
        road_pos = set(road_pos_x + road_pos_y)
        # print(road_pos)

        for x, y in self.grid.empties.copy():
            if not (x in road_pos or y in road_pos):  # not a road -> place building
                building = BuildingAgent(unique_id=self.get_new_unique_id(), model=self, pos=(x, y))
                self.grid.place_agent(building, pos=(x, y))

        # intersections = set((x, y) for x in road_pos_x for y in road_pos_y)
        intersection_pos_x = [building_width * i + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)]
        intersection_pos_y = [building_height * i + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)]
        intersections = set((x, y) for x in intersection_pos_x for y in intersection_pos_y)
        self.intersections = intersections
        print(intersections)
        for intersection_pos in intersections:
            intersection = IntersectionAgent(unique_id=self.get_new_unique_id(), model=self, pos=intersection_pos)
            for traffic_light in intersection.traffic_lights:
                self.grid.place_agent(traffic_light, pos=traffic_light.pos)
        return road_pos, road_pos_x, road_pos_y

    def create_agents(self, road_pos_x, road_pos_y):
        starting_points_top = [(x, self.grid.height-1) for x in road_pos_x if x%2==0]
        starting_points_bottom = [(x, 0) for x in road_pos_x if x%2!=0]

        starting_points_left = [(0, y) for y in road_pos_y if y%2==0]
        starting_points_right = [(self.grid.width-1, y) for y in road_pos_y if y%2!=0]

        starting_points = starting_points_top + starting_points_bottom + starting_points_left + starting_points_right

        end_points_top = [(x, self.grid.height-1) for x in road_pos_x if x%2!=0]
        end_points_bottom = [(x, 0) for x in road_pos_x if x%2!=0]

        end_points_left = [(0, y) for y in road_pos_y if y%2==0]
        end_points_right = [(self.grid.width-1, y) for y in road_pos_y if y%2!=0]

        end_points = end_points_top + end_points_bottom + end_points_left + end_points_right

        for start_point in starting_points:
            if start_point[0] == 0:
                velocity = (1, 0)
            elif start_point[0] == self.grid.height-1:
                velocity = (-1, 0)
            elif start_point[1] == 0:
                velocity = (0, 1)
            else:
                velocity = (0, -1)

            end_point = random.choice(end_points)

            agent = CarAgent(unique_id=self.get_new_unique_id(), model=self, pos=start_point, speed=1, velocity=velocity, destination=end_point)
            self.grid.place_agent(agent, pos=start_point)
            self.agents.append(agent)

    def step(self):
        '''
        Method that steps every agent.

        Prevents applying step on new agents by creating a local list.
        '''
        for agent in list(self.agents):
            agent.step()

if __name__ == '__main__':
    # model = CityModel()
    # model.step()

    # grid = CanvasGrid(agent_portrayal, 100, 108, 540, 540)
    # server = ModularServer(CityModel,
    #                     [grid],
    #                     "City Model")
    # server.port = 8521 # The default
    server.launch()
