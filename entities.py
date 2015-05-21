import pygame
from math import hypot
from random import randint


class Point(object):
    def __init__(self, position, radius=4, color=(0,0,0)):
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
        self.__class__.counter += 1

    def __str__(self):
        return str(self.id) + ": " + super(BusStop, self).__str__()

    def __repr__(self):
        return str(self.id) + ": " + super(BusStop, self).__repr__()


class Path(object):
    def __init__(self):
        self.pheromones = 0
        self.distance = 0


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
            self.color = (randint(0,255), randint(0,255), randint(0,255))
            
        self.__class__.used_colors.append(self.color)