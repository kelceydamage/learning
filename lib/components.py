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
class Cell(object):
	def __init__(self, x, y, reachable, terrain):
		super(Cell, self).__init__()
		self.reachable = reachable
		self.x = x
		self.y = y
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0
		self.terrain = terrain
		self.overlay = None
		self.resources = {
			terrain: random.randint(0, 500)
		}
		self.objects = []

class Cluster(object):
	def __init__(self, args):
		super(Cluster, self).__init__()
		self.construct(args)
		
	def construct(self, args):
		for param in args:
			if param != 'shapes':
				setattr(self, param, args[param])
			else:
				self.shapes = [Shape(args[param][shape]) for shape in args[param]]

class Shape(object):
	def __init__(self, args):
		super(Shape, self).__init__()
		self.length = args['length']
		self.width = args['width']

class Tile(object):
	def __init__(self, args):
		super(Tile, self).__init__()
		self.name = args['name']
		self.layers = args['layers']
		self.recursive = args['recursive']
		self.clusters = []
		self.register_clusters(args['clusters'])

	def register_clusters(self, clusters):
		self.clusters = [Cluster(clusters[x]) for x in clusters]