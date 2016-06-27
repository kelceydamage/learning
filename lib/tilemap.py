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
# Imports
#-----------------------------------------------------------------------#
import random
from components import Cell

# Class
#-----------------------------------------------------------------------#
class Map(object):
	def __init__(self, width, height):
		super(Map, self).__init__()
		self.height = height
		self.width = width
		self.cells = []
		self._map = {}
		self.player_start = []
		self.player_goal = []
		self.old_route_terrain = []
		self.reachable = []
		self.train = False
		self.init_grid()

	def init_grid(self):
		for x in range(self.width):
			for y in range(self.height):
				reachable = True
				terrain = 1
				self.cells.append(Cell(x, y, reachable, terrain))
		self.arrange_grid()

	def arrange_grid(self):
		for c in self.cells:
			if c.x not in self._map.keys():
				self._map[c.x] = {}
				self._map[c.x][c.y] = c
			else:
				self._map[c.x][c.y] = c	

	def regen_cells(self):
		self.cells = []
		for x in self._map:
			for y in self._map[x]:
				self.cells.append(self._map[x][y])

	def display_route(self, route):
		for coord in route:
			tile = self._map[coord[0]][coord[1]].terrain
			self.old_route_terrain.append([coord[0], coord[1], tile])
			x = coord[0]
			y = coord[1]
			if self.train == True:
				self._map[x][y].ptrain = 98
			else:
				self._map[x][y].overlay = 99

	def clean_up_map(self):
		for coord in self.old_route_terrain:
			x = coord[0]
			y = coord[1]
			tile = coord[2]
			self._map[x][y].overlay = None
			self._map[x][y].ptrain = None
		self.old_route_terrain = []

	def start_blob(self, recursion=30):
		if recursion == 0:
			return self.width // 3, self.height // 3
		else:
			recursion -= 1
		try:
			coord = random.randint(0, len(self.reachable))
			return self.reachable[coord]
		except Exception, e:
			t = self.reachable[coord]
			return self.start_blob(recursion)

	def update_reachable(self):
		for x in self._map:
			for y in self._map[x]:
				if self._map[x][y].reachable == True:
					self.reachable.append(self._map[x][y])

