from mesa import Agent


class CarAgent(Agent):
    def __init__(self, unique_id, model, start_pos, stop_pos):
        super().__init__(unique_id, model)
        self.pos = start_pos
        self.end_pos = stop_pos


class BuildingAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
