from entities import BusStop, Bus
from random import randint


class Ants(object):
    def __init__(self, paths, alfa=2):
        self.paths = paths
        self.alfa = alfa

    def divide_stops(self, school, stops):
        bus_stops = list(stops)
        buses = []
        bus = Bus()
        current = school

        while bus_stops:            
            allowed_bus_stops = []
            remaining_dist = bus.max_distance - bus.distance
            remaining_place = bus.max_place - bus.place
            for stop in bus_stops:
                dist = current.paths[stop.id][1].distance
                students = current.paths[stop.id][0].students
                if (dist + stop.paths[0][1].distance <= remaining_dist) and (students <= remaining_place):
                    allowed_bus_stops.append(stop)
                    
            if allowed_bus_stops:
                id = allowed_bus_stops[0].id
                dist = current.paths[id][1].distance
                ranges = [dist^self.alfa]
                for stop in allowed_bus_stops[1:]:
                    id = stop.id
                    dist = current.paths[id][1].distance
                    ranges.append(ranges[-1] + dist^self.alfa)
                    
                r = randint(1, ranges[-1])
                for i in range(len(ranges)):
                    if r < ranges[i]:
                        bus.append(current)
                        current = allowed_bus_stops[i]
                        if current in bus_stops:
                            bus_stops.remove(current)
                            if not bus_stops:
                                bus.append(current)
                                bus.append(school)
                                buses.append(bus)
                        break
            else:
                bus.append(current)
                bus.append(school)
                buses.append(bus)
                bus = Bus()
                current = school
        return buses

    def update_pheromones(self, buses):
        for bus in buses:
            for i in range(len(bus)-1):
                path = bus[i].paths[bus[i+1].id][1]
                path.increase_pheromones(len(bus))

        self.evaporation()

    def evaporation(self):
        for p in self.paths:
            p.pheromones *= 0.8
            if p.pheromones < 1:
                p.pheromones = 1
