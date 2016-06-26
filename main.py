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
import pygame
from pygame.locals import *
import random
from lib.tilemap import Map
from lib.world import WorldConfig, WorldGenerator, map_coast
from lib.pathfinding import AStar
from config.world.constants import *
from config import world

# Functions
#-----------------------------------------------------------------------#
def gen_map(tilemap):
	try:
		for x in range(len(world.config)):
			tilemap = WorldGenerator(world.config[x].params).generate(tilemap)
			if world.config[x].params['draw_coast'] == True:
				tilemap = map_coast(tilemap)
		return tilemap
	except Exception, e:
		return gen_map(tilemap)

def plot_course(playerPos, tilemap, goal=None):
	try:
		if goal == None:
			cell = tilemap.start_blob()
			goal = [cell.x, cell.y]
		route = astar.solve(playerPos, goal, tilemap.cells)
		tilemap.clean_up_map()
		tilemap.display_route(route)
		route.reverse()
		print route
		ready = True
	except Exception, e:
		ready = False
	if ready == False:
		return plot_course(playerPos, tilemap, None)
	else:
		return route, tilemap

# Main
#-----------------------------------------------------------------------#
tilemap = Map(MAPWIDTH, MAPHEIGHT)
tilemap = gen_map(tilemap)
tilemap.regen_cells()
tilemap.update_reachable()
astar = AStar(tilemap.width, tilemap.height)


BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

terrain_names = {
	0: 'Hills',
	1: 'Grass',
	2: 'Water',
	3: 'Forest',
	4: 'Coast',
	5: 'Road',
	8: 'Lowhills',
	9: 'Mountain'
}

speed = {
	0: 100,
	1: 1,
	2: 0,
	3: 60,
	4: 80,
	5: 150,
	7: 150,
	8: 50,
	9: 0
}

colors = {
	HILL: BROWN,
	GRASS: GREEN,
	WATER: BLUE,
	PLAYER: BLACK
}

inventory = {
	HILL: 0,
	GRASS: 0,
	COAST: 0,
	FOREST: 0
}

textures = {
	HILL: pygame.image.load('{0}10hills.png'.format(TEXTURE_PATH)),
	GRASS: pygame.image.load('{0}10grass.png'.format(TEXTURE_PATH)),
	WATER: pygame.image.load('{0}10water.png'.format(TEXTURE_PATH)),
	FOREST: pygame.image.load('{0}10forest.png'.format(TEXTURE_PATH)),
	COAST: pygame.image.load('{0}10coast.png'.format(TEXTURE_PATH)),
	CITY: pygame.image.load('{0}10city.png'.format(TEXTURE_PATH)),
	LOWHILL: pygame.image.load('{0}10lowhills.png'.format(TEXTURE_PATH)),
	MOUNTAIN: pygame.image.load('{0}10mountain.png'.format(TEXTURE_PATH))
}

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*(TILESIZE), MAPHEIGHT*(TILESIZE) + 100))
PLAYER = pygame.image.load('{0}10player.png'.format(TEXTURE_PATH)).convert_alpha()
playerPos = tilemap.player_start
fps_clock = pygame.time.Clock()
fps_clock.tick(24)
DISPLAYSURF.fill(BLACK)

INVFONT = pygame.font.Font('{0}FreeSansBold.ttf'.format(FONT_PATH), 18)

GATHER = 10
TERRAFORM = 100

print len(tilemap._map)
print len(tilemap._map[0])

path = [playerPos]
while True:
	
	placePosition = 10
	meta = tilemap._map[playerPos[0]][playerPos[1]]
	string = 'Coordinates: x={0[1]}, y={0[0]} | Terrain: {1} | Resources: {2} | Inventory: {4} | Objects: {3}'.format(
		(meta.x, meta.y),
		terrain_names[meta.terrain],
		meta.resources,
		meta.objects,
		inventory
		)
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+20))
	placePosition = 10
	meta = tilemap._map[playerPos[0]][playerPos[1]]
	string = 'Gather Rate: {0} | Speed Multiplier {1}%'.format(
		GATHER,
		speed[meta.terrain]
		)
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+60))
	
	for event in pygame.event.get():
		#print event
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if (event.key == K_RIGHT):
				if playerPos[0] < MAPWIDTH and tilemap._map[playerPos[0] + 1][playerPos[1]].terrain != 2:
					playerPos[0] += 1
					print playerPos
			if (event.key == K_LEFT):
				if playerPos[0] > 0 and tilemap._map[playerPos[0] - 1][playerPos[1]].terrain != 2:
					playerPos[0] -= 1
					print playerPos
			if (event.key == K_UP):
				if playerPos[1] > 0 and tilemap._map[playerPos[0]][playerPos[1] - 1].terrain != 2:
					playerPos[1] -= 1
					print playerPos
			if (event.key == K_DOWN):
				if playerPos[1] < MAPHEIGHT and tilemap._map[playerPos[0]][playerPos[1] + 1].terrain != 2:
					playerPos[1] += 1
					print playerPos
			if (event.key == K_SPACE):
				current_tile = tilemap._map[playerPos[0]][playerPos[1]].terrain
				if current_tile <= 4:
					if tilemap[playerPos[0]][playerPos[1]]['resources'][current_tile] > GATHER:
						inventory[current_tile] += GATHER
						tilemap[playerPos[0]][playerPos[1]]['resources'][current_tile] -= GATHER
					elif tilemap[playerPos[0]][playerPos[1]]['resources'][current_tile] == 0:
						pass
					else:
						inventory[current_tile] += 0
						tilemap[playerPos[0]][playerPos[1]]['resources'][current_tile] = 0
						tilemap[playerPos[0]][playerPos[1]]['terrain'] = GRASS
			if (event.key == K_e):
				current_tile = tilemap[playerPos[0]][playerPos[1]]['terrain']
				if current_tile == 1 :
					if tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] < TERRAFORM and inventory[FOREST] > 0:
						inventory[FOREST] -= GATHER
						tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] += GATHER
					elif tilemap[playerPos[0]][playerPos[1]]['terrain'] == FOREST:
						pass
					elif tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] >= TERRAFORM and inventory[FOREST] >= 0:
						inventory[FOREST] -= 0
						tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] = 0
						tilemap[playerPos[0]][playerPos[1]]['terrain'] = FOREST
		elif event.type == MOUSEBUTTONUP:
			new_goal = pygame.mouse.get_pos()
			x = new_goal[0] // TILESIZE
			y = new_goal[1] // TILESIZE
			route, tilemap = plot_course(playerPos, tilemap, (x, y))
			path = route

	playerPos = path.pop(0)
	if len(path) == 0:
		route, tilemap = plot_course(playerPos, tilemap)
		path = route

	for row in range(tilemap.width):
		for column in range(tilemap.height):
			#pygame.draw.rect(DISPLAYSURF, colors[tilemap[row][column]['terrain']], (column*(TILESIZE + PADDING), row*(TILESIZE + PADDING), TILESIZE , TILESIZE ))
			# For textures
			try:
				DISPLAYSURF.blit(textures[tilemap._map[row][column].terrain], (row*TILESIZE, column*TILESIZE))
			except Exception, e:
				pass
			DISPLAYSURF.blit(PLAYER, (playerPos[0]*TILESIZE, playerPos[1]*TILESIZE))

	pygame.display.update()
