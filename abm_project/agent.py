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
        # print("hoi nu begint auto:", self.unique_id, self.pos)
        next_path = self.path[self.pos_i + 1:self.pos_i + self.max_velocity + 1]
        content: [TrafficLightAgent, CarAgent] = self.model.grid.get_cell_list_contents(next_path)
        current = self.model.grid.get_cell_list_contents(self.pos)
        traffic_light = False

        if isinstance(current[0], TrafficLightAgent):
            if current[0].state != 0:
                self.velocity = 0
                return
            else:
                self.accelerate(int(np.ceil(self.max_velocity - self.velocity)/2))

        if content:
            next_obj = content[0]
            distance_to_next = next_path.index(next_obj.pos)
            # if isinstance(next_obj, TrafficLightAgent) and self.velocity > 0: # if velocity > 0 cars stand still before the traffic light
            if isinstance(next_obj, TrafficLightAgent):
                if len(content) > 1:
                    next_car = content[1]
                    if next_car.pos == next_obj.pos:  # next car is on traffic light
                        distance_to_next -= 1
                traffic_light = True

            if self.velocity > 0 and distance_to_next <= self.velocity:  # decelerate based on the closest car
                if traffic_light:
                    distance_to_next += 1
                self.decelerate(distance_to_next)
            # elif self.velocity < self.max_velocity and distance_to_next > 0: # distance to next gone otherwise cars stand still before traffic light
            elif self.velocity < self.max_velocity:
                if traffic_light:
                    distance_to_next += 1
                self.accelerate(np.ceil((self.max_velocity - self.velocity) / 2))
                if self.velocity > distance_to_next:
                    self.velocity = distance_to_next
            else:
                pass
        self.move(next_path)

    def move(self, next_path):
        if self.pos_i + self.velocity >= len(self.path):  # remove agent because it reached the edge
            self.destroy()
        elif self.velocity > 0:
            self.model.grid.move_agent(self, next_path[self.velocity-1])
            self.pos_i += self.velocity
        else:
            pass


class BuildingAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos


class Intersection:
    def __init__(self, unique_id, model, pos):
        self.model = model
        self.unique_id = unique_id
        self.pos = pos
        traffic_light_positions = [(pos[0] - 1, pos[1]),
                                   (pos[0] + 1, pos[1] - 1),
                                   (pos[0] + 2, pos[1] + 1),
                                   (pos[0], pos[1] + 2)]
        self.traffic_lights = [
            TrafficLightAgent(self.model.get_new_unique_id(), self.model, traffic_light_positions[i], self)
            for i in range(4)]
        self.next_green = []

    def step(self):
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
        agents_on_sensor = self.model.grid.get_cell_list_contents(self.pos)
        if len(agents_on_sensor) > 1 and self.state != 0 and isinstance(agents_on_sensor[1], CarAgent) and self not in self.intersection.next_green:
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
