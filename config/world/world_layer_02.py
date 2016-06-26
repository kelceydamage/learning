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
# WorldGen Configs
#-----------------------------------------------------------------------#
params2 = {
	'order': {
		0: 'water',
		1: 'hill',
		2: 'lowhill',
		3: 'mountain',
		4: 'forest'
	},
	WATER: {
		'name': 'water',
		'layers': 6,
		'recursive': False,
		'clusters': {
			0: {
				'size': 8,
				'nodes': 8,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': WATER,
				'base': [
					GRASS
				],
				'shapes': {
					0: {
						'length': 7,
						'width': 2
					},
				}
			}
		}
	},
	HILL: {
		'name': 'hill',
		'layers': 6,
		'recursive': False,
		'clusters': {
			0: {
				'size': 8,
				'nodes': 8,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': True,
				'tile': HILL,
				'base': [
					GRASS
				],
				'shapes': {
					0: {
						'length': 7,
						'width': 2
					},
				}
			}
		}
	}
}