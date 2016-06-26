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
class Abilities(object):
	"""docstring for Abilities"""
	def __init__(self):
		pass
		
	# Retrieve the metadat of the current map tile
	def scan(self):
		return _map[cur_pos[0]][cur_pos[1]]

	# Search the current location for objects or resources
	def search(self, location_meta):
		results = {}
		if len(location_meta['resources']) > 0 :
			results['resources'] = location_meta['resources']
		if len(location_meta['objects']) > 0:
			results['objects'] = location_meta['objects']
		return results

	# Take an object of resource from the current location
	def get(self, results, _type):
		in_hand = results[_type]
		_map[cur_pos[0]][cur_pos[1]][_type] = {}
		results[_type] = {}
		return in_hand

	# Leave an object at the current location
	def drop(self, item, _type):
		_map[cur_pos[0]][cur_pos[1]][_type].append(item)

	# Wait
	def wait(self):
		pass

	# Go to a specific coordinate
	def goto(self, position):
		pass

	# Move in a direction
	def move(direction):
		pass

	# Remember the current location for a specific value
	def chart(self):
		pass



