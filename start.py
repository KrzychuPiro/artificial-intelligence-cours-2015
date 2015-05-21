import pygame
from pygame.locals import *
from sys import exit
from entities import BusStop
from ai_algorithms.ants import Ants
from ai_algorithms.tabu import Tabu


class City(object):
    pygame.init()
    
    def __init__(self):
        self.bus_stops = []
        self.school = BusStop((300, 250), color=(255, 255, 255), radius = 7)
        self.school.students = 0
        self.screen = pygame.display.set_mode((600, 500))

    def create_bus_stops(self):
        keep = None
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)
                    
                klawisze = pygame.key.get_pressed()

                if event.type == MOUSEBUTTONUP:
                    keep = None

                elif event.type == MOUSEBUTTONDOWN:
                    for p in self.bus_stops:
                        if p.is_inside(event.pos):
                            if event.button == 3:
                                self.bus_stops.remove(p)
                            else:
                                keep=p
                            break

                    if not keep and event.button != 3:
                        nowe_punkty = []
                        self.bus_stops.append(BusStop(event.pos))

                elif event.type == MOUSEMOTION and keep:
                    keep.position = event.pos

                if klawisze[K_LCTRL] and klawisze[K_n]:
                    self.bus_stops = []
                    BusStop.counter = 1
                if klawisze[K_LCTRL] and klawisze[K_b]:
                    return
            self.display_update()

    def display_update(self):
        self.screen.fill((150, 230, 255))
        self.school.draw(self.screen)  
        for i in self.bus_stops:
            i.draw(self.screen)
        pygame.display.update()

    def run(self):        
        self.create_bus_stops()
        # TODO: create paths

        run = True
        ants = Ants(self.bus_stops)
        tabu = Tabu()

        while run:
            buses = ants.divide_stops()
            self.display_update()
            raw_input()

            tabu.sort_stops(buses)
            # TODO: paths update
            self.display_update()
            run = 'end' != raw_input()
        
        
if __name__ == '__main__':
    c = City()
    c.run()





