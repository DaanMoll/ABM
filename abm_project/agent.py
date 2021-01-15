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

        if content:
            distance_to_next_car = next_path.index(content[0].pos)
            if self.velocity > 0 and distance_to_next_car < self.velocity:  # decelerate based on the closest car
                self.decelerate(distance_to_next_car)
        elif self.velocity < self.max_velocity:
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
