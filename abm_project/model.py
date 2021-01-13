import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import BaseScheduler

from abm_project.agent import CarAgent, BuildingAgent

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

        self.grid = SingleGrid(width=total_width, height=total_height, torus=False)

        self.create_buildings()

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
        print(road_pos)

        for x, y in self.grid.empties.copy():
            if not (x in road_pos or y in road_pos):  # not a road -> place building
                building = BuildingAgent(unique_id=self.get_new_unique_id(), model=self, pos=(x, y))
                self.grid.place_agent(building, pos=(x, y))

    def create_agent(self):
        pass


if __name__ == '__main__':
    model = CityModel()
