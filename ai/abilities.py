#!/usr/bin/env python
# Author: Kelcey Jamison-Damage
# Python: 2.66 +
# OS: CentOS | Other
# Portable: True
# License: Apache 2.0

# License
#-----------------------------------------------------------------------#
# Copyright [2016] [Kelcey Jamison-Damage]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-----------------------------------------------------------------------#
# Class
#-----------------------------------------------------------------------#
class Experience(object):
	"""docstring for Experience"""
	def __init__(self):
		super(Experience, self).__init__()

class Memory(object):
	"""docstring for Memory"""
	def __init__(self):
		super(Memory, self).__init__()
		self.resource_locations = {}
		self.scratchpad = {}
		self.locations = []

class Abilities(object):
	"""docstring for Abilities"""
	def __init__(self, pathfinder):
		self.recursion = 30
		self.pathfinder = pathfinder
		self.memory = Memory()
		self.target = None
		self.position = None
		self.move_speed = 0
		self.enroute = False
		self.route_times = (0, 0)

	def convert_coords(self, cell):
		return (cell.x, cell.y)
		
	# Retrieve the metadat of the current map tile
	def scan(self, tilemap, target):
		path, route, destination, tilemap = self.plot_course(tilemap, scan=True, target=target)
		return route, destination, tilemap

	# Search the current location for objects or resources
	def search(self, tilemap, target):
		def calc_distance(coord1, coord2):
			if coord1[0] > coord2[0]:
				x_distance = coord1[0] - coord2[0]
			else:
				x_distance = coord2[0] - coord1[0]
			if coord1[1] > coord2[1]:
				y_distance = coord1[1] - coord2[1]
			else:
				y_distance = coord2[1] - coord1[1]
			return x_distance + y_distance
		self.memory.scratchpad = {}
		self.memory.resource_locations = self.learn(target, self.memory.resource_locations)
		if len(self.memory.resource_locations[target]) > 0:
			for place in self.memory.resource_locations[target]:
				score = calc_distance(self.convert_coords(place), self.position)
				print 'SCORE', score
				self.memory.scratchpad[score] = place
				print 'MIN', min(self.memory.scratchpad.keys())
			if score > 1 and score < 19:
				closest = self.memory.scratchpad[min(self.memory.scratchpad.keys())]
				route, destination, tilemap = self.goto(tilemap, self.convert_coords(closest))
			else:
				route, destination, tilemap = self.scan(tilemap, target)
		else:
			route, destination, tilemap = self.scan(tilemap, target)
		self.enroute = True
		return route, destination, tilemap

	# Take an object of resource from the current location
	def get(self, results, _type):
		in_hand = results[_type]
		_map[cur_pos[0]][cur_pos[1]][_type] = {}
		results[_type] = {}
		return in_hand

	def mine(self):
		pass

	# Leave an object at the current location
	def drop(self, item, _type):
		_map[cur_pos[0]][cur_pos[1]][_type].append(item)

	# Wait
	def wait(self):
		pass

	# Go to a specific coordinate
	def goto(self, tilemap, goal):
		path, route, destination, tilemap = self.plot_course(tilemap, goal=goal)
		return route, destination, tilemap

	# Move in a direction
	def move(self, route, destination, tilemap):
		if self.move_speed != 0:
			self.move_speed -= 1
		else:
			if len(route) == 0:
				self.position = destination
				self.enroute = False
			else:
				self.position = route.pop(0)
			self.move_speed = tilemap.speed[tilemap._map[self.position[0]][self.position[1]].terrain][1] * 5

	# Remember the current location for a specific value
	def chart(self):
		pass

	def learn(self, new, existing):
		if new not in existing:
			existing[new] = []
		return existing

	def time_to_destination(self, route, tilemap):
		return sum([tilemap.speed[tilemap._map[x[0]][x[1]].terrain][1] * 5 for x in route])

	def plot_course(self, tilemap, goal=None, scan=False, target=1):
		if self.recursion == 0:
			return None, None, tilemap
		else:
			self.recursion -= 1
		try:
			if goal == None:
				cell = tilemap.start_blob()
				goal = [cell.x, cell.y]
			path, route = self.pathfinder.solve(self.position, goal, tilemap.cells, scan=scan, target=target, train=False)
			path, train = self.pathfinder.solve(self.position, goal, tilemap.cells, scan=scan, target=target, train=True)
			destination = self.pathfinder.path_local(tilemap.cells, tilemap._map[path[1][0]][path[1][1]], target)
			if scan == False:
				self.memory.locations.append(tilemap._map[train[-1][0]][train[-1][1]])
			else:
				self.memory.resource_locations = self.learn(target, self.memory.resource_locations)
				if target in tilemap._map[train[-1][0]][train[-1][1]].resources:
					self.memory.resource_locations[target].append(tilemap._map[train[-1][0]][train[-1][1]])
			tilemap.clean_up_map()
			tilemap.display_route(route)
			tilemap.train = True
			tilemap.display_route(train)
			tilemap.train = False
			route.reverse()
			train.reverse()
			h_time = self.time_to_destination(route, tilemap)
			s_time = self.time_to_destination(train, tilemap)
			path = []
			if h_time > s_time:
				route = train
			self.recursion = 30
			self.route_times = (h_time, s_time)
			return path, route, destination, tilemap
		except Exception, e:
			return self.plot_course(tilemap, goal=None, scan=scan, target=target)



