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
from constants import *

# WorldGen Configs
#-----------------------------------------------------------------------#
params = {
	'order': {
		0: 'water',
		1: 'hill',
		2: 'lowhill',
		3: 'mountain',
		4: 'forest'
	},
	'draw_coast': True,
	WATER: {
		'name': 'water',
		'layers': 3,
		'recursive': False,
		'clusters': {
			0: {
				'size': 20,
				'nodes': 80,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': WATER,
				'base': [
					WATER,
					GRASS
				],
				'shapes': {
					0: {
						'length': 7,
						'width': 1
					},
					1: {
						'length': 3,
						'width': 5
					},
				}
			},
			1: {
				'size': 5,
				'nodes': 1,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': WATER,
				'base': [
					WATER,
					GRASS
				],
				'shapes': {
					0: {
						'length': 25,
						'width': 12
					}
				}
			},
			2: {
				'size': 20,
				'nodes': 30,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': WATER,
				'base': [
					WATER,
					GRASS
				],
				'shapes': {
					0: {
						'length': 2,
						'width': 5
					}
				}
			},
			3: {
				'size': 3,
				'nodes': 1,
				'x_shift': +20,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': WATER,
				'base': [
					WATER,
					GRASS
				],
				'shapes': {
					0: {
						'length': 30,
						'width': 2
					}
				}
			},
			4: {
				'size': 10,
				'nodes': 30,
				'x_shift': +30,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': WATER,
				'base': [
					WATER,
					GRASS
				],
				'shapes': {
					0: {
						'length': 4,
						'width': 3
					}
				}
			}
		}
	},
	HILL: {
		'name': 'hill',
		'layers': 12,
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
			},
			1: {
				'size': 4,
				'nodes': 10,
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
						'length': 2,
						'width': 5
					},
				}
			}
		}
	},
	LOWHILL: {
		'name': 'lowhill',
		'layers': 12,
		'recursive': True,
		'clusters': {
			0: {
				'size': 8,
				'nodes': 10,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': True,
				'tile': LOWHILL,
				'base': [
					GRASS
				],
				'shapes': {
					0: {
						'length': 7,
						'width': 2
					},
				}
			},
			1: {
				'size': 4,
				'nodes': 10,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': True,
				'tile': LOWHILL,
				'base': [
					GRASS
				],
				'shapes': {
					0: {
						'length': 7,
						'width': 6
					},
				}
			}
		}
	},
	MOUNTAIN: {
		'name': 'mountain',
		'layers': 12,
		'recursive': True,
		'clusters': {
			0: {
				'size': 5,
				'nodes': 5,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': False,
				'tile': MOUNTAIN,
				'base': [
					GRASS,
					LOWHILL
				],
				'shapes': {
					0: {
						'length': 3,
						'width': 2
					},
				}
			},
			1: {
				'size': 5,
				'nodes': 3,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': True,
				'reachable': False,
				'tile': MOUNTAIN,
				'base': [
					GRASS,
					LOWHILL,
					HILL
				],
				'shapes': {
					0: {
						'length': 5,
						'width': 1
					},
				}
			}
		}
	},
	FOREST: {
		'name': 'forest',
		'layers': 20,
		'recursive': False,
		'clusters': {
			0: {
				'size': 8,
				'nodes': 8,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': True,
				'tile': FOREST,
				'base': [
					GRASS,
					LOWHILL
				],
				'shapes': {
					0: {
						'length': 7,
						'width': 2
					},
				}
			},
			1: {
				'size': 4,
				'nodes': 10,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': True,
				'reachable': True,
				'tile': FOREST,
				'base': [
					GRASS,
					LOWHILL,
					FOREST
				],
				'shapes': {
					0: {
						'length': 5,
						'width': 7
					},
				}
			},
			2: {
				'size': 4,
				'nodes': 10,
				'x_shift': 0,
				'y_shift': 0,
				'recursive': False,
				'reachable': True,
				'tile': FOREST,
				'base': [
					GRASS,
					LOWHILL
				],
				'shapes': {
					0: {
						'length': 5,
						'width': 2
					},
				}
			}
		}
	}
}