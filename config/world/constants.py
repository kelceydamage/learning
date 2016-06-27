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


# Constants
#-----------------------------------------------------------------------#
TILESIZE 		= 10
MAPWIDTH 		= 160
MAPHEIGHT 		= 80
PADDING 		= 0
TEXTURE_PATH 	= 'art/tiles/'
FONT_PATH 		= 'art/fonts/'

# Terrain
#-----------------------------------------------------------------------#
HILL			= 0
GRASS			= 1
WATER			= 2
FOREST			= 3
COAST			= 4
CITY			= 5
LOWHILL			= 8
MOUNTAIN		= 9
PLAYER	 		= 6
ROAD			= 7
#PATH			= 99
TERRAIN_NAMES = {
	0: 			'Hills',
	1: 			'Grass',
	2: 			'Water',
	3: 			'Forest',
	4: 			'Coast',
	5:			'City',
	7: 			'Road',
	8: 			'Lowhills',
	9: 			'Mountain'
}
TEXTURES = {
	HILL: 		'{0}10hills.png'.format(TEXTURE_PATH),
	GRASS: 		'{0}10grass.png'.format(TEXTURE_PATH),
	WATER: 		'{0}10water.png'.format(TEXTURE_PATH),
	FOREST: 	'{0}10forest.png'.format(TEXTURE_PATH),
	COAST: 		'{0}10coast.png'.format(TEXTURE_PATH),
	CITY: 		'{0}10city.png'.format(TEXTURE_PATH),
	LOWHILL: 	'{0}10lowhills.png'.format(TEXTURE_PATH),
	MOUNTAIN: 	'{0}10mountain.png'.format(TEXTURE_PATH),
	ROAD:		'{0}10road.png'.format(TEXTURE_PATH)
}
PLAYER 			= '{0}10player.png'.format(TEXTURE_PATH)
PATH 			= '{0}10path.png'.format(TEXTURE_PATH)
PTRAIN			= '{0}10ptrain.png'.format(TEXTURE_PATH)

# Colors
#-----------------------------------------------------------------------#
BROWN 			= (153, 76, 0)
GREEN 			= (0, 255, 0)
BLUE 			= (0, 0, 255)
BLACK 			= (0, 0, 0)
WHITE 			= (255, 255, 255)
R 				= (0, 60, 255)
COLORS = {
	HILL: BROWN,
	GRASS: GREEN,
	WATER: BLUE,
	PLAYER: BLACK,
	PATH: R
}

# Inventory
#-----------------------------------------------------------------------#
INVENTORY = {
	HILL: 		0,
	GRASS: 		0,
	COAST: 		0,
	FOREST: 	0
}