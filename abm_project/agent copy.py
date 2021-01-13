from mesa import Agent

import numpy as np
import operator
import random


class CarAgent(Agent):
    def __init__(self, model, unique_id, pos, velocity, velocity_vector, destination):
        super().__init__(unique_id, model)
        self.pos = pos
        self.velocity = velocity
        self.vectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        self.velocity_vector = velocity_vector
        self.destination = destination # not being used yet

        self.turning = False
        self.turning_counter = 0

        matrix = np.array([
            ["s", None, "l", "r"],
            [None, "s", "l", "r"],

        ]
        )

        print(matrix[0])

    def step(self):
        if self.turning:
            if self.turning_counter == 0:
                self.new_vector = random.choice(self.vectors)
                while self.new_vector == tuple([x * -1 for x in self.velocity_vector]):
                    self.new_vector = random.choice(self.vectors)

                if self.new_vector == self.velocity_vector:
                    self.turn = "straight"
                elif sum(self.new_vector) == sum(self.velocity_vector):
                    self.turn = "left"
                else:
                    self.turn = "right"
                print(self.turn, self.velocity_vector, self.new_vector)
            elif self.turning_counter == 1:
                self.velocity = 1
            elif self.turning_counter == 2:
                if self.turn == "right":
                    self.velocity_vector = self.new_vector
                    self.turning = False
            elif self.turning_counter == 3:
                if self.turn == "left":
                    self.velocity_vector = self.new_vector
                else:
                    self.turning = False
            elif self.turning_counter == 4:
                self.turning = False

            print(self.turning_counter)
            self.turning_counter += 1
                
        if self.velocity != 0:
            print("velocityvector", self.velocity_vector)
            change = tuple([x * self.velocity for x in self.velocity_vector])
            next_pos = tuple(map(operator.add, self.pos, change))

            if not self.turning:
                intersection = False
                while next_pos in self.model.intersections:
                    intersection = True
                    self.velocity -= 1 # if velocity increases > 1
                    print("hoi")
                    change = tuple([x * self.velocity for x in self.velocity_vector])
                    next_pos = tuple(map(operator.add, self.pos, change))
            
                if intersection:
                    self.velocity = 0
                    self.turning = True
                    self.turning_counter = 0
            
            self.model.grid.move_agent(self, next_pos)


class BuildingAgent(Agent):
    def __init__(self, unique_id, pos):
        super().__init__(unique_id, pos)
