from mesa import Agent

import numpy as np
import operator
import random


class CarAgent(Agent):
    def __init__(self, model, unique_id, pos, velocity, velocity_vector, destination):
        super().__init__(unique_id, model)
        self.pos = pos
        self.velocity = velocity
        self.directions = ["s", "l", "r"]
        self.vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        self.velocity_vector = velocity_vector
        self.destination = destination # not being used yet

        self.turning = False
        self.turning_counter = 0

    def step(self):
        if self.turning:
            if self.turning_counter == 0:
                self.turn = random.choice(self.directions)
                for i in range(len(self.vectors)):
                    if self.vectors[i] == self.velocity_vector:
                        if self.turn == "r":
                            self.new_vector = self.vectors[(i+1)%len(self.vectors)]
                        elif self.turn == "l":
                            self.new_vector = self.vectors[i-1]
                        else:
                            self.new_vector = self.velocity_vector
            elif self.turning_counter == 1:
                self.velocity = 1
            elif self.turning_counter == 2:
                if self.turn == "r":
                    self.velocity_vector = self.new_vector
                    self.turning = False
            elif self.turning_counter == 3:
                if self.turn == "l":
                    self.velocity_vector = self.new_vector
                else:
                    self.turning = False
            elif self.turning_counter == 4:
                self.turning = False

            self.turning_counter += 1
                
        if self.velocity != 0:
            change = tuple([x * self.velocity for x in self.velocity_vector])
            next_pos = tuple(map(operator.add, self.pos, change))

            if not self.turning:
                intersection = False
                while next_pos in self.model.intersections:
                    intersection = True
                    # self.velocity -= 1 # if velocity increases > 1
                    change = tuple([x * self.velocity for x in self.velocity_vector])
                    next_pos = tuple(map(operator.add, self.pos, change))
            
                if intersection:
                    self.velocity = 0
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
