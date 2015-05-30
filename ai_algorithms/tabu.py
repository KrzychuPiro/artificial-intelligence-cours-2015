from entities import BusStop, Bus
from math import sqrt

class Tabu(object):

	def sort_stops(self, buses):
		new_buses = []
		for bus in buses:
			new_buses.append(self._get_best_path(bus))
		return new_buses

	def _get_best_path(self,buses):
		all_buses_perm = self.permu(buses[1:-1])
		sums = []
		for perm in all_buses_perm:
			sums.append(self._get_path_weight(perm))
		best_perm = all_buses_perm[sums.index(min(sums))]
		best_perm.insert(0, buses[0])
		best_perm.insert(len(best_perm), buses[0])
		bus_list = Bus()
		for el in best_perm:
			bus_list.append(el)
		return bus_list

	def _get_path_weight(self, perm):
		sum_d = 0
		for index, current_bus in enumerate(perm):
			try:
				index+=1
				c_x = perm[index].position[0]
				c_y = perm[index].position[1]
				next_x = perm[index-1].position[0]
				next_y = perm[index-1].position[1]
				d = sqrt((abs(c_x-next_x))^2+(abs(c_y-next_y))^2)
				sum_d += d
			except IndexError:
				pass
		return sum_d

	def permu(self, xs):
		if xs:
			r , h = [],[]
			for x in xs:
				if x not in h:
					ts = xs[:]; ts.remove(x)
					for p in self.permu(ts):
						r.append([x]+p)
				h.append(x)
			return r
		else:
			return [[]]

