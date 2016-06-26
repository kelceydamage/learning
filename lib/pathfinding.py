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
import heapq

# Class
#-----------------------------------------------------------------------#
class AStar(object):
	def __init__(self, grid_width, grid_height):
		super(AStar, self).__init__()
		self.opened = []
		heapq.heapify(self.opened)
		self.closed = set()
		self.cells = []
		self.grid_height = grid_height
		self.grid_width = grid_width
		self.route = []
		self.weights = {
			0: 40,
			1: 10,
			2: 0,
			3: 30,
			4: 15,
			5: 5,
			7: 150,
			8: 20,
			9: 0
		}

	def re_init(self):
		self.opened = []
		heapq.heapify(self.opened)
		self.closed = set()
		self.cells = []
		self.route = []

	def get_heuristics(self, cell):
		val = self.weights[cell.terrain]
		h = val * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
		return h

	def get_cell(self, x, y):
		try:
			return self.cells[x * self.grid_height + y]
		except Exception, e:
			print 'Cell Len', len(self.cells), 'Cell Fetch', (x * self.grid_height + y), (x, self.grid_height, y)
			print 'Get Cell', x, y, e
			print x * self.grid_height + y
			print len(self.cells)

	def get_adjacent_cells(self, cell):
		def validate(n_cell, cell, r):
			if n_cell == None:
				print r, (cell.x, cell.y), 
			return n_cell
		cells = []
		if cell.x < self.grid_width - 1:
			n_cell = validate(self.get_cell(cell.x + 1, cell.y), cell, 0)
			cells.append(n_cell)
		if cell.y > 0:
			n_cell = validate(self.get_cell(cell.x, cell.y - 1), cell, 1)
			cells.append(n_cell)
		if cell.x > 0:
			n_cell = validate(self.get_cell(cell.x - 1, cell.y), cell, 2)
			cells.append(n_cell)
		if cell.y < self.grid_height - 1:
			n_cell = validate(self.get_cell(cell.x, cell.y + 1), cell, 3)
			cells.append(n_cell)
		if cell.y > 0 and cell.x > 0:
			n_cell = validate(self.get_cell(cell.x - 1, cell.y - 1), cell, 4)
			cells.append(n_cell)
		if cell.y < self.grid_width - 1 and cell.x < self.grid_height - 1:
			n_cell = validate(self.get_cell(cell.x + 1, cell.y + 1), cell, 5)
			cells.append(n_cell)
		if cell.y > 0 and cell.x < self.grid_width - 1:
			n_cell = validate(self.get_cell(cell.x + 1, cell.y - 1), cell, 6)
			cells.append(n_cell)
		if cell.y < self.grid_height - 1 and cell.x > 0:
			n_cell = validate(self.get_cell(cell.x - 1, cell.y + 1), cell, 7)
			cells.append(n_cell)
		return cells

	def get_path(self):
		cell = self.end
		path = [(cell.x, cell.y)]
		while cell.parent is not self.start:
			cell = cell.parent
			self.route.append((cell.x, cell.y))
		path.append((self.start.x, self.start.y))
		path.reverse()
		return path, self.route

	def update_cell(self, adj, cell):
		adj.g = cell.g + 10
		adj.h = self.get_heuristics(adj)
		adj.parent = cell
		adj.f = adj.h + adj.g

	def solve(self, start, end, cells):
		self.re_init()
		self.cells = cells
		self.start = self.get_cell(start[0], start[1])
		self.end = self.get_cell(end[0], end[1])
		# add starting cell to open heap queue
		print 'START', self.start.x, self.start.y, self.end.x, self.end.y
		heapq.heappush(self.opened, (self.start.f, self.start))
		while len(self.opened):
			if not self.end.reachable:
				print ((self.end.x, self.end.y),), ((0,0),)
				return ((self.end.x, self.end.y),), ((0,0),)
			# pop cell from heap queue
			f, cell = heapq.heappop(self.opened)
			# add cell to closed list so we don't process it twice
			self.closed.add(cell)
			# if ending cell, return found path
			if cell is self.end:
				path, route = self.get_path()
				self.re_init()
				return route

			adj_cells = self.get_adjacent_cells(cell)
			for adj_cell in adj_cells:
				if adj_cell.reachable and adj_cell not in self.closed:
					if (adj_cell.f, adj_cell) in self.opened:
						if adj_cell.g > cell.g + 10:
							self.update_cell(adj_cell, cell)
					else:
						self.update_cell(adj_cell, cell)
						heapq.heappush(self.opened, (adj_cell.f, adj_cell))





