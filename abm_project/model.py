import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from mesa import Model
from mesa.space import SingleGrid, MultiGrid
from mesa.time import BaseScheduler
from scipy.spatial.distance import euclidean
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
        self.schedule = BaseScheduler(self)
        self.grid = MultiGrid(width=total_width, height=total_height, torus=False)
        road_pos = self.create_buildings()
        # create buildings, then road map becasue it uses empty cell list
        self.road_graph = self.create_road_graph()
        # then create intersections otherwise graph doesnt work
        # Currently still needed for traffic lights
        self.agents = []
        self.create_intersections()

        self.starting_points = self.get_starting_points(road_pos[1], road_pos[2])
        self.end_points = self.get_end_points(road_pos[1], road_pos[2])
        self.max_car_agents = 100
        self.num_car_agents = 0

        for i in range(5):
            self.create_car_agent()

    def get_new_unique_id(self):
        self.unique_id += 1
        return self.unique_id

    def create_buildings(self):
        """
        Populates area between roads with buildings.
        """
        self.intersections = []

        road_pos_x = [building_width * i + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)] + \
                     [building_width * i + 1 + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)]
        road_pos_y = [building_height * i + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)] + \
                     [building_height * i + 1 + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)]
        road_pos = set(road_pos_x + road_pos_y)

        for x, y in self.grid.empties.copy():
            if not (x in road_pos or y in road_pos):  # not a road -> place building
                building = BuildingAgent(unique_id=self.get_new_unique_id(), model=self, pos=(x, y))
                self.grid.place_agent(building, pos=(x, y))

        return road_pos, road_pos_x, road_pos_y

    def create_intersections(self):
        intersection_pos_x = [building_width * i + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)]
        intersection_pos_y = [building_height * i + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)]
        intersections = set((x, y) for x in intersection_pos_x for y in intersection_pos_y)

        for intersection_pos in intersections:
            intersection = IntersectionAgent(unique_id=self.get_new_unique_id(), model=self, pos=intersection_pos)
            self.intersections.append(intersection)
            self.schedule.add(intersection)

            for traffic_light in intersection.traffic_lights:
                self.grid.place_agent(traffic_light, pos=traffic_light.pos)
                self.schedule.add(traffic_light)
                self.agents.append(traffic_light)

    def get_starting_points(self, road_pos_x, road_pos_y):
        starting_points_top = [(x, self.grid.height - 1) for x in road_pos_x if x % 2 == 0]
        starting_points_bottom = [(x, 0) for x in road_pos_x if x % 2 != 0]

        starting_points_left = [(0, y) for y in road_pos_y if y % 2 == 0]
        starting_points_right = [(self.grid.width - 1, y) for y in road_pos_y if y % 2 != 0]

        return starting_points_top + starting_points_bottom + starting_points_left + starting_points_right

    def get_end_points(self, road_pos_x, road_pos_y):
        end_points_top = [(x, self.grid.height - 1) for x in road_pos_x if x % 2 != 0]
        end_points_bottom = [(x, 0) for x in road_pos_x if x % 2 == 0]

        end_points_left = [(0, y) for y in road_pos_y if y % 2 != 0]
        end_points_right = [(self.grid.width - 1, y) for y in road_pos_y if y % 2 == 0]

        return end_points_top + end_points_bottom + end_points_left + end_points_right

    def create_car_agent(self):
        start_point = random.choice(self.starting_points)
        # start_point = self.starting_points[0]
        while not self.grid.is_cell_empty(start_point):  # if the starting cell is not empty, pick a new one
            start_point = random.choice(self.starting_points)

        distance = 0
        while distance < road_width:
            end_point = random.choice([point for point in self.end_points if point is not start_point])
            distance = euclidean(end_point, start_point)

        path = random.choice(list(nx.all_shortest_paths(self.road_graph, start_point, end_point)))

        agent = CarAgent(unique_id=self.get_new_unique_id(), model=self, path=path, max_velocity=5)

        self.grid.place_agent(agent, pos=path[0])
        self.schedule.add(agent)
        self.num_car_agents += 1

    def step(self):
        self.schedule.step()
        if self.num_car_agents < self.max_car_agents:
            for _ in range(5):
                self.create_car_agent()

    def create_road_graph(self, draw=False):
        graph = nx.DiGraph()

        roads = list(self.grid.empties)
        roads.sort()

        horizontal_paths_index = [n_roads_horizontal * building_height * road_width * i
                                  + road_width * total_width * (i - 1)
                                  for i in range(1, n_roads_vertical + 1)]

        horizontal_paths_left = [roads[i:i + total_width] for i in horizontal_paths_index]
        horizontal_paths_right = [roads[i + total_width:i + 2 * total_width] for i in horizontal_paths_index]

        vertical_paths_down = [[(y, x) for x, y in road] for road in horizontal_paths_left]
        vertical_paths_up = [[(y, x) for x, y in road] for road in horizontal_paths_right]

        reversed = horizontal_paths_left + vertical_paths_up
        unchanged = horizontal_paths_right + vertical_paths_down
        combined = reversed + unchanged

        for path in reversed:
            nx.add_path(graph, path)
        graph = graph.reverse()
        for path in unchanged:
            nx.add_path(graph, path)

        if draw:
            positions = {coord: coord for path in combined for coord in path}
            nx.draw(graph, pos=positions, node_size=100)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.show()

        # get shortest path using nx.shortest_path(graph, (0, 86), (20, 0))
        return graph


if __name__ == '__main__':
    model = CityModel()
    model.step()