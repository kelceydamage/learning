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
from ai.abilities import *
from config.game.configuration import *
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

# Main
#-----------------------------------------------------------------------#
tilemap = Map(MAPWIDTH, MAPHEIGHT)
tilemap = gen_map(tilemap)
tilemap.speed = SPEED
tilemap.regen_cells()
tilemap.update_reachable()
astar = AStar(tilemap.width, tilemap.height)
abilities = Abilities(astar)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*(TILESIZE), MAPHEIGHT*(TILESIZE) + 250))
PLAYER = pygame.image.load(PLAYER).convert_alpha()
PATH = pygame.image.load(PATH).convert_alpha()
PTRAIN = pygame.image.load(PTRAIN).convert_alpha()
for texture in TEXTURES:
	TEXTURES[texture] = pygame.image.load(TEXTURES[texture])
playerPos = tilemap.player_start
fps_clock = pygame.time.Clock()
fps_clock.tick(10)
DISPLAYSURF.fill(BLACK)

INVFONT = pygame.font.Font('{0}FreeSansBold.ttf'.format(FONT_PATH), 14)

gather = INIT_GATHER
terraform = INIT_TERRAFORM

wait = 0
path = [playerPos]
destination = playerPos
turns = 0
h_time = 0
s_time = 0
while True:
	abilities.position = playerPos
	turns += 1
	
	placePosition = 10
	meta = tilemap._map[playerPos[0]][playerPos[1]]
	string = 'Turns: {0}'.format(turns) + ' ' * 100
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE))
	string = 'Coordinates: x={0}, y={1}'.format(meta.x, meta.y) + ' ' * 100
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+20))
	string = 'Terrain: {0}'.format(TERRAIN_NAMES[meta.terrain] + ' ' * 100)
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+40))
	string = 'Resources: {0}'.format(str(meta.resources) + ' ' * 100)
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+60))
	string = 'Inventory: {0}'.format(str(INVENTORY) + ' ' * 100)
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+80))
	meta = tilemap._map[playerPos[0]][playerPos[1]]
	string = 'Gather Rate: {0}'.format(str(gather) + ' ' * 100)
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+100))
	string = 'Speed Penalty: {0}% | Heuristic: {1} | Turns To Cross: {2}'.format(
		round(SPEED[meta.terrain][1] / float(SPEED[GRASS][1]), 2) * 100, SPEED[meta.terrain][0], SPEED[meta.terrain][1] * 5
		) + ' ' * 100
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+120))
	string = 'Turns To Destination(Heuristic): {0} | Turns To Destination(ShortestPath): {1}'.format(abilities.route_times[0], abilities.route_times[1]) + ' ' * 100
	textObj = INVFONT.render(string, True, WHITE, BLACK) 
	DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+140))

	for event in pygame.event.get():
		#print event
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if (event.key == K_RIGHT):
				if playerPos[0] < MAPWIDTH and tilemap._map[playerPos[0] + 1][playerPos[1]].terrain != 2:
					playerPos[0] += 1
			if (event.key == K_LEFT):
				if playerPos[0] > 0 and tilemap._map[playerPos[0] - 1][playerPos[1]].terrain != 2:
					playerPos[0] -= 1
			if (event.key == K_UP):
				if playerPos[1] > 0 and tilemap._map[playerPos[0]][playerPos[1] - 1].terrain != 2:
					playerPos[1] -= 1
			if (event.key == K_DOWN):
				if playerPos[1] < MAPHEIGHT and tilemap._map[playerPos[0]][playerPos[1] + 1].terrain != 2:
					playerPos[1] += 1
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
					if tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] < terraform and inventory[FOREST] > 0:
						inventory[FOREST] -= GATHER
						tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] += GATHER
					elif tilemap[playerPos[0]][playerPos[1]]['terrain'] == FOREST:
						pass
					elif tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] >= terraform and inventory[FOREST] >= 0:
						inventory[FOREST] -= 0
						tilemap[playerPos[0]][playerPos[1]]['resources'][FOREST] = 0
						tilemap[playerPos[0]][playerPos[1]]['terrain'] = FOREST
		elif event.type == MOUSEBUTTONUP:
			new_goal = pygame.mouse.get_pos()
			x = new_goal[0] // TILESIZE
			y = new_goal[1] // TILESIZE
			path, route, destination, tilemap = abilities.plot_course(tilemap, goal=(x, y))
			abilities.move(route, destination, tilemap)
			playerPos = abilities.position

	if abilities.enroute == False:
		route, destination, tilemap = abilities.search(tilemap, HILL)
		print abilities.memory.scratchpad
	else:
		abilities.move(route, destination, tilemap)
		playerPos = abilities.position

	for row in range(tilemap.width):
		for column in range(tilemap.height):
			#pygame.draw.rect(DISPLAYSURF, colors[tilemap[row][column]['terrain']], (column*(TILESIZE + PADDING), row*(TILESIZE + PADDING), TILESIZE , TILESIZE ))
			# For textures
			try:
				DISPLAYSURF.blit(TEXTURES[tilemap._map[row][column].terrain], (row*TILESIZE, column*TILESIZE))
				if tilemap._map[row][column].overlay != None:
					DISPLAYSURF.blit(PATH, (row*TILESIZE, column*TILESIZE))
				elif tilemap._map[row][column].ptrain != None:
					DISPLAYSURF.blit(PTRAIN, (row*TILESIZE, column*TILESIZE))
			except Exception, e:
				pass
			DISPLAYSURF.blit(PLAYER, (playerPos[0]*TILESIZE, playerPos[1]*TILESIZE))


	pygame.display.update()
