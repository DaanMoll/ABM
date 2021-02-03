import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import pickle
import random

from tqdm import tqdm
from mesa import Model
from mesa.space import SingleGrid, MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from scipy.spatial.distance import euclidean
from agent import CarAgent, BuildingAgent, IntersectionAgent

'''

This file describes the main model, CityModel, and all its functions:

- Intersection, building and car agent creators as well road graph creator
- Grid initializer
- Road graph generator
- Data collector functions

Usage:

- Instantiate the model using model = CityModel(green_light_duration=gld, max_car_agents=max_cars_agents,
                              tolerance=tolerance)
- Run the model for a desired number of steps using model.step()
- Collect the output: data = model.datacollector.get_model_vars_dataframe()
'''

n_roads_horizontal = 4
n_roads_vertical = 4

road_width = 2

building_width = 20
building_height = 20

total_width = building_width * \
              (n_roads_horizontal + 1) + n_roads_horizontal * road_width
total_height = building_height * \
               (n_roads_vertical + 1) + n_roads_vertical * road_width

random.seed(1)
np.random.seed(1)


class CityModel(Model):
    ''' Creates a City Model

    Arguments:
        max_car_agents: maximum amount of cars in the grid at a given time step
        cars_per_second: amount of cars that enter the grid per second until max_car_agents is reached
        max_velocity: starting maximum velocity for car agents
        tolerance: congestion threshold that will cause a caragent to be "hasty"
        green_light_duration: amount of steps a given traffic light agent will stay red or green

    The model collects "AverageCongestion" and "HastePercent" at each step, which can be retrieved through model.datacollector.get_model_vars_dataframe()
    '''
    def __init__(self, max_car_agents=100, cars_per_second=5, max_velocity=5, tolerance=1, green_light_duration=5):
        super().__init__()
        self.max_car_agents = max_car_agents
        self.cars_per_second = cars_per_second
        self.green_light_duration = green_light_duration
        self.tolerance = tolerance

        self.agents = []
        self.intersections = []
        self.unique_id = 0
        self.num_car_agents = 0
        self.max_velocity = max_velocity

        self.datacollector = DataCollector(model_reporters={
            "AverageCongestion": self.get_average_congestion,
            "HastePercent": self.get_average_haste
        })

        self.schedule = BaseScheduler(self)
        self.grid = MultiGrid(width=total_width, height=total_height, torus=False)
        self.road_graph, self.starting_points, self.end_points = self.initialize_grid()

    def get_average_congestion(self):
        all_congestion = [agent.congestion for agent in self.schedule.agents if isinstance(agent, CarAgent)]
        return 100 - 100 * (sum(all_congestion) / len(all_congestion))

    def get_average_haste(self):
        all_haste = [agent.haste for agent in self.schedule.agents if isinstance(agent, CarAgent)]
        return 100 * np.mean(all_haste)

    def get_new_unique_id(self):
        self.unique_id += 1
        return self.unique_id

    def initialize_grid(self):
        road_pos = self.create_buildings()
        road_graph = self.create_road_graph()
        self.create_intersections()
        starting_points = self.get_starting_points(road_pos[1], road_pos[2])
        end_points = self.get_end_points(road_pos[1], road_pos[2])
        return road_graph, starting_points, end_points

    def create_buildings(self):
        """
        Populates area between roads with buildings.
        """

        road_pos_x = [building_width * i + road_width * (i - 1) for i in range(1, n_roads_horizontal + 1)] + \
                     [building_width * i + 1 + road_width *
                      (i - 1) for i in range(1, n_roads_horizontal + 1)]
        road_pos_y = [building_height * i + road_width * (i - 1) for i in range(1, n_roads_vertical + 1)] + \
                     [building_height * i + 1 + road_width *
                      (i - 1) for i in range(1, n_roads_vertical + 1)]
        road_pos = set(road_pos_x + road_pos_y)

        for x, y in self.grid.empties.copy():
            if not (x in road_pos or y in road_pos):  # not a road -> place building
                building = BuildingAgent(
                    unique_id=self.get_new_unique_id(), model=self, pos=(x, y))
                self.grid.place_agent(building, pos=(x, y))

        return road_pos, road_pos_x, road_pos_y

    def create_intersections(self):
        intersection_pos_x = [building_width * i + road_width *
                              (i - 1) for i in range(1, n_roads_horizontal + 1)]
        intersection_pos_y = [building_height * i + road_width *
                              (i - 1) for i in range(1, n_roads_vertical + 1)]
        intersections = set((x, y)
                            for x in intersection_pos_x for y in intersection_pos_y)

        for intersection_pos in intersections:
            intersection = IntersectionAgent(unique_id=self.get_new_unique_id(),
                                             model=self,
                                             pos=intersection_pos,
                                             green_light_duration=self.green_light_duration)
            self.intersections.append(intersection)
            self.schedule.add(intersection)

            for traffic_light in intersection.traffic_lights:
                self.grid.place_agent(traffic_light, pos=traffic_light.pos)
                self.schedule.add(traffic_light)
                self.agents.append(traffic_light)

    def get_starting_points(self, road_pos_x, road_pos_y):
        starting_points_top = [(x, self.grid.height - 1)
                               for x in road_pos_x if x % 2 == 0]
        starting_points_bottom = [(x, 0) for x in road_pos_x if x % 2 != 0]

        starting_points_left = [(0, y) for y in road_pos_y if y % 2 == 0]
        starting_points_right = [(self.grid.width - 1, y)
                                 for y in road_pos_y if y % 2 != 0]

        return starting_points_top + starting_points_bottom + starting_points_left + starting_points_right

    def get_end_points(self, road_pos_x, road_pos_y):
        end_points_top = [(x, self.grid.height - 1)
                          for x in road_pos_x if x % 2 != 0]
        end_points_bottom = [(x, 0) for x in road_pos_x if x % 2 == 0]

        end_points_left = [(0, y) for y in road_pos_y if y % 2 != 0]
        end_points_right = [(self.grid.width - 1, y)
                            for y in road_pos_y if y % 2 == 0]

        return end_points_top + end_points_bottom + end_points_left + end_points_right

    def create_car_agent(self):
        start_point = random.choice(self.starting_points)
        # if the starting cell is not empty, pick a new one
        while not self.grid.is_cell_empty(start_point):
            start_point = random.choice(self.starting_points)

        distance = 0
        while distance < road_width:
            end_point = random.choice(
                [point for point in self.end_points if point is not start_point])
            distance = euclidean(end_point, start_point)

        path = random.choice(list(nx.all_shortest_paths(
            self.road_graph, start_point, end_point)))

        agent = CarAgent(unique_id=self.get_new_unique_id(),
                         model=self, path=path, max_velocity=self.max_velocity, tolerance=self.tolerance)

        self.grid.place_agent(agent, pos=path[0])
        self.schedule.add(agent)
        self.num_car_agents += 1

    def step(self):
        ''' Advances the model by one step and if the maximum amount of car agents hasn't been reached 
        car_per_second agents will be generated'''

        self.schedule.step()
        if self.num_car_agents < self.max_car_agents:
            for _ in range(self.cars_per_second):
                self.create_car_agent()
        self.datacollector.collect(self)

    def create_road_graph(self, draw=False):
        graph = nx.DiGraph()

        roads = list(self.grid.empties)
        roads.sort()

        horizontal_paths_index = [n_roads_horizontal * building_height * road_width * i
                                  + road_width * total_width * (i - 1)
                                  for i in range(1, n_roads_vertical + 1)]

        horizontal_paths_left = [roads[i:i + total_width]
                                 for i in horizontal_paths_index]
        horizontal_paths_right = [
            roads[i + total_width:i + 2 * total_width] for i in horizontal_paths_index]

        vertical_paths_down = [[(y, x) for x, y in road]
                               for road in horizontal_paths_left]
        vertical_paths_up = [[(y, x) for x, y in road]
                             for road in horizontal_paths_right]

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


def run_experiment(number_iterations, max_steps, experiment_name, green_light_duration, max_cars_agents,
                   tolerance):
    """ Takes:
        number of runs, maximum steps per run and experiment name +
        parameters (max_velocity, green_light_duration,green_light_duration, max_cars_agents, tolerance)

        Outputs a list with all the runs congestions data, with the last element of the list being the model parameters,
        Saves the output as "experiment_name.p" and returns it
    """
    tolerances = [0, 0.25, 0.5, 0.75, 1]
    car_agents = [10, 20, 50, 100, 200]
    green_light_duration = [2, 3, 5, 7, 8]
    all_data = [green_light_duration]
    for gld in green_light_duration:
        for _ in tqdm(range(number_iterations)):
            model = CityModel(green_light_duration=gld, max_car_agents=max_cars_agents,
                              tolerance=tolerance)
            for _ in range(max_steps):
                model.step()

            # Returns a pandas.DataFrame
            data = model.datacollector.get_model_vars_dataframe()
            data = data.iloc[:, 0].values
            all_data.append(data)

    # The final output is a list with all of the congestion data from each run,
    # in a list object, and the parameters of the run as the last item of the list, in a dic
    name = experiment_name + ".pickle"
    pickle.dump(all_data, open(name, "wb"))
    return all_data


def stats(data):
    mean = np.average(data[0:-1])
    std = np.std(data[0:-1])
    counter = 0
    all_grid_lock = []
    for l in data[0:-1]:
        if l[-2] > mean + std:
            counter += 1
            all_grid_lock.append(l)
    mean_lock = np.average(all_grid_lock)
    print("Mean: ", mean, "Std: ", std, "Mean Jam: ",
          mean_lock, "Number of jams: ", counter, "-", counter / len(data[0:-1]), "%")
    return all_grid_lock


def main():
    iterations = 1000
    steps = 1000
    green_light_duration = ""
    max_car_agents = 150
    tolerance = 0.2

    experiment_name = f'data_i{iterations}_s{steps}_gld{green_light_duration}_mca{max_car_agents}_t{str(tolerance).replace(".", "")}'
    print(experiment_name)
    run_experiment(number_iterations=iterations,
                   max_steps=steps,
                   experiment_name=experiment_name,
                   green_light_duration=green_light_duration,
                   max_cars_agents=max_car_agents,
                   tolerance=tolerance)
    all_data = pickle.load(open(experiment_name + ".pickle", "rb"))
    # for _data in all_data:
    #     if isinstance(_data, list):
    #         plt.plot(_data[10:len(_data)])
    # plt.show()
    #
    # locks = stats(all_data)
    # for _data in locks:
    #     plt.plot(_data)
    # plt.show()

    car_agents = all_data.pop(0)
    all_data = np.array(all_data).reshape((len(car_agents), iterations, steps))
    for i, data_var in enumerate(all_data):
        mean = np.mean(data_var, axis=0)
        std = np.std(data_var, axis=0)
        xs = range(mean.size)

        plt.plot(xs, mean, label=car_agents[i])
        plt.fill_between(xs, mean - std, mean + std, alpha=0.2)
    plt.xlabel("Timesteps")
    plt.ylabel("Congestion")
    plt.title(f"{iterations} iterations, tolerance={tolerance}, green light duration = {green_light_duration}")
    plt.xlim(xs[0], xs[-1]+1)
    plt.ylim(0, 100)
    plt.legend(title="max car agents")
    plt.show()


if __name__ == '__main__':
    main()
