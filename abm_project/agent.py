from mesa import Agent

import numpy as np


class CarAgent(Agent):
    def __init__(self, model, unique_id, path, max_velocity):
        super().__init__(unique_id, model)
        self.path = path
        self.pos_i = 0
        self.pos = path[self.pos_i]
        self.max_velocity = max_velocity
        self.velocity = max_velocity

    def accelerate(self, amount):
        self.velocity += int(amount)

    def decelerate(self, distance):
        if distance > 0:
            self.velocity = int(np.ceil(distance / 2))
        else:
            self.velocity = 0

    def destroy(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.num_car_agents -= 1

    def step(self):
        next_path = self.path[self.pos_i + 1:self.pos_i + self.max_velocity + 1]
        content: [CarAgent] = self.model.grid.get_cell_list_contents(next_path)
        
        current = self.model.grid.get_cell_list_contents(self.pos)
        # check if waiting for traffic_light
        if len(current) > 1:
            for agent in current:
                if type(agent) == TrafficLightAgent:
                    if agent.state != 0:
                        self.waiting = True
                    else:
                        self.waiting = False   

        if content:
            if type(content[0]) == CarAgent:
                distance_to_next_car = next_path.index(content[0].pos)
                if self.velocity > 0 and distance_to_next_car < self.velocity:  # decelerate based on the closest car
                    self.decelerate(distance_to_next_car)
            elif type(content[0]) == TrafficLightAgent:
                # so seeing traffic light so check if other cars on that cell
                content_light = self.model.grid.get_cell_list_contents(content[0].pos)
                if len(content_light) > 1: # car on cell
                    pos_i = self.path.index(content[0].pos) - 1
                    self.model.grid.move_agent(self, self.path[pos_i])
                    self.waiting = True
                # so light is yellow or red
                elif content[0].state != 0:
                    # distance_to_light = next_path.index(content[0].pos)
                    self.model.grid.move_agent(self, content[0].pos)
                    self.velocity = 0
                    self.pos_i = self.path.index(content[0].pos)
                    self.waiting = True

        if self.velocity < self.max_velocity and not self.waiting:
            self.accelerate(np.ceil((self.max_velocity - self.velocity) / 2))

        if self.pos_i + self.velocity >= len(self.path):  # remove agent because it reached the edge
            self.destroy()
        elif self.velocity > 0:
            self.model.grid.move_agent(self, next_path[self.velocity-1])
            self.pos_i += self.velocity

class BuildingAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

class Intersection():
    def __init__(self, unique_id, model, pos):
        self.model = model
        self.unique_id = unique_id
        self.pos = pos
        traffic_light_positions = [(pos[0] - 1, pos[1]),
                                   (pos[0] + 1, pos[1] - 1),
                                   (pos[0] + 2, pos[1] + 1),
                                   (pos[0], pos[1] + 2)]
        
        self.traffic_lights = []
        for i in range(4):
            agent = TrafficLightAgent(self.model.get_new_unique_id(), self.model, traffic_light_positions[i], self)
            self.traffic_lights.append(agent)
        #     self.model.grid.place_agent(agent, traffic_light_positions[i])

        self.next_green = []

    def step(self):
        if len(self.next_green) > 0:
            print(len(self.next_green), self.next_green, self.next_green[0].pos)
        if all(traffic_light.state == 2 for traffic_light in self.traffic_lights) and len(self.next_green) > 0:
            next_traffic_light = self.next_green.pop(0)
            next_traffic_light.state = 0

class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, pos, intersection):
        super().__init__(unique_id, model)
        self.colors = {0: 'green', 1: 'yellow', 2: 'red'}
        self.state = 2
        self.pos = pos
        self.timer = 5
        self.intersection = intersection

    def step(self):
        self.state = 2
        agents_on_sensor = self.model.grid.get_cell_list_contents(self.pos)

        if len(agents_on_sensor) > 1 and type(agents_on_sensor[1]) == CarAgent and self.state != 0 and self not in self.intersection.next_green:
            self.intersection.next_green.append(self)

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
