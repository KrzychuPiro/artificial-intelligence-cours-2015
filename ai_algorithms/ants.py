from entities import BusStop, Bus


class Ants(object):
    def divide_stops(self, school, stops):
        buses = []
        b = Bus()
        b.append(school)

        # ******** example *********
        for i in xrange(len(stops)):
            b.append(stops[i])
            if i % 4 == 3:
                b.append(school)
                buses.append(b)
                b = Bus()
                b.append(school)
        if b not in buses and len(b)>1:
            b.append(school)
            buses.append(b)
        # **************************

        return buses
