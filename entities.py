import pygame
from math import hypot
from random import randint


class Point(object):
    def __init__(self, position, radius=4, color=(0, 0, 0)):
        self.position = position
        self.radius = radius
        self.color = color

    def is_inside(self, pos):
        x, y = self.position
        return hypot(x-pos[0], y-pos[1]) <= self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius, 0)

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self.position)


class BusStop(Point):
    counter = 0

    def __init__(self, *args, **kwargs):
        super(BusStop, self).__init__(*args, **kwargs)
        self.students = randint(1, 15)
        self.id = self.counter
        self.paths = {}
        self.__class__.counter += 1

    def update_paths(self):
        for key in self.paths:
            self.paths[key][1].update_distance(self, self.paths[key][0])

    def evaporation(self):
        for p in self.paths:
            self.paths[p][1].evaporation()

    def draw(self, surface):
        super(BusStop, self).draw(surface)
        for p in self.paths:
            pygame.draw.line(surface, self.color, self.position, self.paths[p][0].position, self.paths[p][1].pheromones)

    def __str__(self):
        return str(self.id) + ": " + super(BusStop, self).__str__()

    def __repr__(self):
        return str(self.id) + ": " + super(BusStop, self).__repr__()


class Path(object):
    def __init__(self, p1, p2):
        self.pheromones = 0
        self.update_distance(p1, p2)

    def update_distance(self, p1, p2):
        self.distance = int(hypot(p1.position[0]-p2.position[0], p1.position[1]-p2.position[1]))
        return self.distance

    def increase_pheromones(self):
        self.pheromones += 3

    def evaporation(self):
        self.pheromones -= 1
        if self.pheromones < 0: self.pheromones = 0

    def __str__(self):
        return "Path(%i)" % self.distance

    def __repr__(self):
        return "Path(%i)" % self.distance


class Bus(list):
    max_distance = 1000
    max_place = 50

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
              (255,255,0), (255,0,255), (0,255,255),
              (0, 255, 175), (0, 175, 255),
              (175, 0, 255), (255, 0, 175),
              (255, 175, 0), (175, 0, 255)]
    used_colors = []
    
    def __init__(self, *args, **kwargs):
        super(Bus, self).__init__(*args, **kwargs)
        self.distance = 0
        self.place = 0
        self.take_color()

    def take_color(self):
        if self.colors:
            r = randint(0, len(self.colors)-1)
            self.color = self.colors[r]
            self.__class__.colors.remove(self.color)
        else:
            self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.__class__.used_colors.append(self.color)

    def update_pheromones(self):
        for i in range(len(self)-1):
            self[i].paths[self[i+1].id][1].increase_pheromones()

    def append(self, item):
        if not(len(self) == 0 or item == self[0]):
            item.color = self.color
        super(Bus, self).append(item)