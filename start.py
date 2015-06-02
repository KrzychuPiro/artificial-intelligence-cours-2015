import pygame
from pygame.locals import *
from sys import exit
from entities import BusStop, Path, Bus
from ai_algorithms.ants import Ants
from ai_algorithms.tabu import Tabu


class City(object):
    pygame.init()
    
    def __init__(self):
        self.bus_stops = []
        self.school = BusStop((300, 250), color=(255, 255, 255), radius=7)
        self.school.students = 0
        self.screen = pygame.display.set_mode((600, 550))
        self.buses = []
        self.iteration = 0

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
        if self.buses:
            for bus in self.buses:
                bus.draw(self.screen)
        else:
            for i in range(1, 7):
                pygame.draw.circle(self.screen, (127, 127, 127), self.school.position, i*50, 1)
            for i in self.bus_stops:
                i.draw(self.screen)

        for b in self.bus_stops:
            b.students_draw(self.screen)
        self.school.draw(self.screen)

        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(0, 500, 600, 50))
        dist_txt = "Max Time: %s" % Bus.max_distance
        place_txt = "Max Capacity: %s" % Bus.max_place
        count_txt = "Buses: %s" % str(len(self.buses))
        iter_txt = "Iteration: %s" % str(self.iteration)

        dist = pygame.font.SysFont("segoe print", 15).render(dist_txt, True, (0, 0, 0))
        place = pygame.font.SysFont("segoe print", 15).render(place_txt, True, (0, 0, 0))
        count = pygame.font.SysFont("segoe print", 15).render(count_txt, True, (0, 0, 0))
        iter = pygame.font.SysFont("segoe print", 15).render(iter_txt, True, (0, 0, 0))

        self.screen.blit(dist, (10, 502))
        self.screen.blit(place, (10, 525))
        self.screen.blit(count, (490, 502))
        self.screen.blit(iter, (490, 525))
        pygame.display.update()

    def run(self):        
        self.create_bus_stops()
        self.paths = set()
        for bus in self.bus_stops:
            self.paths.update(set(path[1] for path in bus.paths.values()))
        run = True
        step = 1
        jump = 0
        ants = Ants(self.paths)
        tabu = Tabu()
        best = len(self.bus_stops)

        while run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 3:
                        jump += 1
                        step = (step + 1) % 4
                    else:
                        step = (step + 1) % 4

            if jump:
                if jump < 100:
                    jump += 1
                    step = (step + 1) % 4
                else:
                    jump = 0
                    step = (step + 1) % 4

            if step == 1:
                print 'step 1 ', step
                self.iteration += 1
                current = best+1
                while current > best:
                    self.buses = ants.divide_stops(self.school, self.bus_stops)
                    current = len(self.buses)
                best = current
                step += 1
            elif step == 3:
                print 'step 3 ', step
                self.buses = tabu.sort_stops(self.buses)
                ants.update_pheromones(self.buses)
                step += 1
            self.display_update()
            self.buses[0].reset()

        pygame.display.quit()
        return self.buses

        
if __name__ == '__main__':
    c = City()
    print c.run()





