import pygame
from pygame.locals import *
from sys import exit
from entities import BusStop, Path
from ai_algorithms.ants import Ants
from ai_algorithms.tabu import Tabu


class City(object):
    pygame.init()
    
    def __init__(self):
        self.bus_stops = []
        self.school = BusStop((300, 250), color=(255, 255, 255), radius=7)
        self.school.students = 0
        self.screen = pygame.display.set_mode((600, 500))

    def create_bus_stops(self):
        def add_bus_stop():
            bs = BusStop(event.pos)
            path = Path(bs, self.school)
            bs.paths[0] = [self.school, path]
            self.school.paths[bs.id] = [bs, path]
            for p in self.bus_stops:
                path = Path(bs, p)
                p.paths[bs.id] = [bs, path]
                bs.paths[p.id] = [p, path]
            self.bus_stops.append(bs)

        def remove_bus_stop(stop):
            self.bus_stops.remove(stop)
            del self.school.paths[stop.id]
            for b in self.bus_stops:
                del b.paths[stop.id]
            del stop

        keep = None
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)

                if event.type == MOUSEBUTTONUP and keep:
                    keep.update_paths()
                    keep = None

                elif event.type == MOUSEBUTTONDOWN:
                    for p in self.bus_stops:
                        if p.is_inside(event.pos):
                            if event.button == 3:
                                remove_bus_stop(p)
                            else:
                                keep = p
                            break
                    if not keep and event.button != 3:
                        add_bus_stop()

                elif event.type == MOUSEMOTION and keep:
                    keep.position = event.pos

                else:
                    keys = pygame.key.get_pressed()
                    if keys[K_LCTRL] and keys[K_n]:
                        self.school.paths = {}
                        self.bus_stops = []
                        BusStop.counter = 1
                    if keys[K_LCTRL] and keys[K_b]:
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

        run = True
        step = 1
        ants = Ants()
        tabu = Tabu()
        buses = []

        while run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False

                if event.type == MOUSEBUTTONDOWN:
                    step = (step + 1) % 4

            if step == 1:
                buses = ants.divide_stops(self.school, self.bus_stops)
                step += 1
            elif step == 3:
                buses = tabu.sort_stops(buses)
                for b in buses:
                    b.update_pheromones()
                for s in self.bus_stops:
                    s.evaporation()
                step += 1
            self.display_update()

        pygame.display.quit()
        return buses
        
        
if __name__ == '__main__':
    c = City()
    print c.run()





