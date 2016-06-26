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

# Class
#-----------------------------------------------------------------------#
class WorldConfig(object):
	def __init__(self, params):
		super(WorldConfig, self).__init__()
		self.tiles = []
		self.construct(params)
	
	def construct(self, params):
		self.tile_types = [Tile(params[x]) for x in params if x != 'order']
		self.order = params['order']
		
class WorldGenerator(object):
	def __init__(self, params):
		super(WorldGenerator, self).__init__()
		self.config = WorldConfig(params)
		self.previous_layers = []
		self.prev_cluster = []
		self.temp = []
		
	def generate(self, tilemap):
		self.tilemap = tilemap
		for i in range(len(self.config.order)):
			for tile_type in self.config.tile_types:
				if tile_type.name == self.config.order[i]:
					self.draw_layers(tile_type)
		self.tilemap.player_start = list(self.start_blob(self.tilemap.width, self.tilemap.height))
		self.tilemap.player_goal = list(self.start_blob(self.tilemap.width, self.tilemap.height))
		return self.tilemap

	def draw_layers(self, tile_type):
		for i in range(tile_type.layers):
			if tile_type.recursive == True:
				coord = self.previous_layers[i]; x = coord[0]; y = coord[1]
			else:
				x, y = self.start_blob(self.tilemap.width, self.tilemap.height)
			for cluster_config in tile_type.clusters:
				if cluster_config.recursive == True:
					cluster = self.prev_cluster
					self.prev_cluster = []
				else:
					cluster = self.define_cluster(cluster_config, x, y)
					self.prev_cluster = cluster
				shapes = self.generate_shapes(cluster, cluster_config.shapes)
				self.merge(shapes, cluster_config)
			self.temp.append((x, y))
		self.previous_layers = self.temp
		self.temp = []

	def generate_shapes(self, cluster, blueprints):
		shapes = []
		for shape_config in blueprints:
			shapes.append([self.form(coord, shape_config) for coord in cluster])
		return shapes

	def start_blob(self, x_max, y_max, x_min=0, y_min=0, recursion=30, base=[1], nodes=None):
		if recursion == 0:
			return self.tilemap.width // 3, self.tilemap.height // 3
		else:
			recursion -= 1
		x = random.randint(x_min, x_max - 1)
		y = random.randint(y_min, y_max - 1)
		if self.tilemap._map[x][y].terrain in base:
			return x, y
		else:
			return self.start_blob(x_max, y_max, x_min, y_min, recursion, base, nodes=nodes)
		
	def define_cluster(self, cluster_config, x, y, recursion=30):
		cluster = []
		base = cluster_config.base
		if cluster_config.x_shift != 0:
			x += cluster_config.x_shift
		if cluster_config.y_shift != 0:
			y += cluster_config.y_shift
		x_max = x + cluster_config.size
		y_max = y + cluster_config.size
		x_min = x - cluster_config.size
		y_min = y - cluster_config.size
		if x_max > self.tilemap.width - 1: x_max = self.tilemap.width - 1		
		if y_max > self.tilemap.height - 1: y_max = self.tilemap.height - 1
		if x_max <= x_min: x_min -= 10
		if y_max <= y_min: y_min -= 10
		if x_min < 0: x_min = 0	
		if y_min < 0: y_min = 0
		for i in range(cluster_config.nodes):
			cluster.append(self.start_blob(x_max, y_max, x_min, y_min, recursion, base, nodes=cluster_config.nodes))
		return cluster

	def form(self, coord, shape_config):
		def draw_line(shape, old_pos, w, n):
			shape.append([old_pos[0] + n, old_pos[1]])
			for i in range(1, w + 1):
				shape.append([old_pos[0] + n, old_pos[1] + i])
				shape.append([old_pos[0] + n, old_pos[1] - i])
			return shape

		old_pos = tuple(coord)
		shape = []
		p = 1
		for n in range(shape_config.length):
			if n == shape_config.length - 1:
				w = random.randint(1, (shape_config.width // 3) + 1)
			elif n == shape_config.length - 2:
				w = random.randint(p, (shape_config.width // 2) + 1); p = shape_config.width // 3
			elif n == shape_config.length - 3:
				w = random.randint(p, (shape_config.width // 1.5) + 1); p = shape_config.width // 2
			elif n == 2:
				w = random.randint(p, (shape_config.width // 1.5) + 1); p = w
			elif n == 1:
				w = random.randint(p, (shape_config.width // 2) + 1); p = w
			elif n == 0:
				w = random.randint(1, (shape_config.width // 3) + 1); p = w
			else:
				w = random.randint(p, shape_config.width + 1)
			shape = draw_line(shape, old_pos, w, n)
		return shape

	def merge(self, shapes, cluster_config):
		def validate_coords(shape, cluster_config):
			merge_list = []
			for coord in shape:
				x = coord[0]
				y = coord[1]
				if x < self.tilemap.width and y < self.tilemap.height and y >= 0:
					if self.tilemap._map[x][y].terrain in cluster_config.base:
						merge_list.append((x, y))
			return merge_list

		def update_map(cluster_config, c):
			self.tilemap._map[c[0]][c[1]].terrain = cluster_config.tile
			self.tilemap._map[c[0]][c[1]].resources[cluster_config.tile] = random.randint(0, 500)
			self.tilemap._map[c[0]][c[1]].reachable = cluster_config.reachable

		for shape in shapes:
			for shape_map in shape:
					merge_list = validate_coords(shape_map, cluster_config)
					[update_map(cluster_config, coord) for coord in merge_list]

def map_coast(tilemap):
	def check_neighbours(x, y, tilemap):
		t1 = 1
		t2 = 1
		if x == 0 or y == 0:
			pass
		elif x == tilemap.width - 1 or y == tilemap.height - 1:
			pass
		else:
			if tilemap._map[x + 1][y].terrain == t1 \
			or tilemap._map[x + 1][y].terrain == t2:
				tilemap._map[x + 1][y].terrain = 4
			if tilemap._map[x + 1][y + 1].terrain == t1 \
			or tilemap._map[x + 1][y + 1].terrain == t2:
				tilemap._map[x + 1][y + 1].terrain = 4
			if tilemap._map[x][y + 1].terrain == t1 \
			or tilemap._map[x][y + 1].terrain == t2:
				tilemap._map[x][y + 1].terrain = 4
			if tilemap._map[x - 1][y + 1].terrain == t1 \
			or tilemap._map[x - 1][y + 1].terrain == t2:
				tilemap._map[x - 1][y + 1].terrain = 4
			if tilemap._map[x - 1][y].terrain == t1 \
			or tilemap._map[x - 1][y].terrain == t2:
				tilemap._map[x - 1][y].terrain = 4
			if tilemap._map[x - 1][y - 1].terrain == t1 \
			or tilemap._map[x - 1][y - 1].terrain == t2:
				tilemap._map[x - 1][y - 1].terrain = 4
			if tilemap._map[x][y - 1].terrain == t1 \
			or tilemap._map[x][y - 1].terrain == t2:
				tilemap._map[x][y - 1].terrain = 4
			if tilemap._map[x + 1][y - 1].terrain == t1 \
			or tilemap._map[x + 1][y - 1].terrain == t2:
				tilemap._map[x + 1][y - 1].terrain = 4
		return tilemap

	for x in tilemap._map:
		for y in tilemap._map[x]:
			if tilemap._map[x][y].terrain == 2:
				tilemap = check_neighbours(x, y, tilemap)
	return tilemap