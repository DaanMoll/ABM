from mesa import Model
from mesa.space import SingleGrid
from mesa.time import BaseScheduler

from abm_project.agent import CarAgent, BuildingAgent

n_roads_horizontal = 4
n_roads_vertical = 4

road_width = 2

distance_roads_hortizontal = 20
distance_roads_vertical = 20


class CityModel(Model):

    def __init__(self):
        super().__init__()
        self.unique_id = 0

        self.grid = SingleGrid(width=distance_roads_hortizontal * (n_roads_horizontal+1) + n_roads_horizontal * road_width,
                               height=distance_roads_vertical * (n_roads_vertical+1) + n_roads_vertical * road_width,
                               torus=False)

        self.create_buildings()

    def get_new_unique_id(self):
        self.unique_id += 1
        return self.unique_id

    def create_buildings(self):
        """
        Populates area between roads with buildings.
        """
        road_pos_x = [distance_roads_hortizontal * i + 1 for i in range(1, n_roads_horizontal + 1)] + \
                     [distance_roads_hortizontal * i + 2 for i in range(1, n_roads_horizontal + 1)]
        road_pos_y = [distance_roads_vertical * i + 1 for i in range(1, n_roads_vertical + 1)] + \
                     [distance_roads_vertical * i + 2 for i in range(1, n_roads_vertical + 1)]
        road_pos = set(road_pos_x + road_pos_y)

        for x, y in self.grid.empties.copy():
            if not (x in road_pos or y in road_pos):  # not a road -> building
                building = BuildingAgent(unique_id=self.get_new_unique_id(), pos=(x, y))
                self.grid.place_agent(building, pos=(x, y))

    def create_agent(self):
        pass


if __name__ == '__main__':
    model = CityModel()
