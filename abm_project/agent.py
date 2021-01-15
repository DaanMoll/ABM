from mesa import Agent

import numpy as np
import operator
import random


class CarAgent(Agent):
    def __init__(self, model, unique_id, pos, speed, velocity, destination):
        super().__init__(unique_id, model)
        self.pos = pos
        self.speed = speed
        self.directions = ["s", "l", "r"]
        self.vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self.velocity = velocity
        self.destination = destination # not being used yet

        self.turning = False
        self.turning_counter = 0

    def step(self):
        if self.turning:
            if self.turning_counter == 0:
                self.turn = random.choice(self.directions)
                for i in range(len(self.vectors)):
                    if self.vectors[i] == self.velocity:
                        if self.turn == "r":
                            self.new_vector = self.vectors[(i+1)%len(self.vectors)]
                        elif self.turn == "l":
                            self.new_vector = self.vectors[i-1]
                        else:
                            self.new_vector = self.velocity
            elif self.turning_counter == 1:
                self.speed = 1
            elif self.turning_counter == 2:
                if self.turn == "r":
                    self.velocity = self.new_vector
                    self.turning = False
            elif self.turning_counter == 3:
                if self.turn == "l":
                    self.velocity = self.new_vector
                else:
                    self.turning = False
            elif self.turning_counter == 4:
                self.turning = False

            self.turning_counter += 1

        if self.speed != 0:
            change = tuple([x * self.speed for x in self.velocity])
            next_pos = tuple(map(operator.add, self.pos, change))

            if not self.turning:
                intersection = False
                while next_pos in self.model.intersections:
                    intersection = True
                    self.speed -= 1 # if speed increases > 1
                    change = tuple([x * self.speed for x in self.velocity])
                    next_pos = tuple(map(operator.add, self.pos, change))

                if intersection:
                    self.speed = 0
                    self.turning = True
                    self.turning_counter = 0

            if self.model.grid.is_cell_empty(next_pos):
                if self.turning:
                    self.turning_counter -= 1
                self.model.grid.move_agent(self, next_pos)

class BuildingAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos


class IntersectionAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        traffic_light_positions = [(pos[0] - 1, pos[1]),
                                   (pos[0] + 1, pos[1] - 1),
                                   (pos[0] + 2, pos[1] + 1),
                                   (pos[0], pos[1] + 2)]
        sensor_positions = [(traffic_light_positions[0][0] - 1, traffic_light_positions[0][1]),
                            (traffic_light_positions[1][0], traffic_light_positions[1][1] - 1),
                            (traffic_light_positions[2][0] + 1, traffic_light_positions[2][1]),
                            (traffic_light_positions[3][0], traffic_light_positions[3][1] + 1)]
        self.traffic_lights = [
            TrafficLightAgent(unique_id, model, traffic_light_positions[i], self, sensor_positions[i])
            for i in range(4)]
        self.next_green = []

    def step(self):
        if all(traffic_light.state == 2 for traffic_light in self.traffic_lights) and len(self.next_green) > 0:
            next_traffic_light = self.next_green.pop(0)
            next_traffic_light.state = 0


class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, pos, intersection_agent, sensor_position):
        super().__init__(unique_id, model)
        self.colors = {0: 'green', 1: 'yellow', 2: 'red'}
        self.state = 2
        self.pos = pos
        self.timer = 5
        self.intersection_agent = intersection_agent
        self.sensor_position = sensor_position

    def step(self):
        agents_on_sensor = self.model.grid.get_neighbors(self.sensor_position, radius=0, moore=False, include_center=True)
        if len(agents_on_sensor) > 0 and type(agents_on_sensor[0]) == CarAgent and self not in self.intersection_agent.next_green:
            self.intersection_agent.next_green.append(self)

        if self.state == 0:
            if self.timer <= 0:
                self.state = 1
                self.timer = 2
            else:
                self.timer -= 1
        elif self.state == 1:
            if self.timer <= 0:
                self.state = 2
                self.timer = 5
            else:
                self.timer -= 1
