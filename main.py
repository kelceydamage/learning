#!/usr/bin/env python

import pygame
from pygame.locals import *
import random
from generators import Map, WorldGenerator, WorldConfig, map_coast
from a_star import AStar
from world_config import *

def gen_map(tilemap):
	try:
		tilemap = WorldGenerator(params).generate(tilemap)
		tilemap = map_coast(tilemap)
		tilemap = WorldGenerator(params2).generate(tilemap)
		ready = True
	except Exception, e:
		ready = False
	if ready == False:
		return gen_map(tilemap)
	else:
		return tilemap

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

tilemap = Map(MAPWIDTH, MAPHEIGHT)
tilemap = gen_map(tilemap)
gx = tilemap.player_goal[0]
gy = tilemap.player_goal[1]
tilemap._map[gx][gy].terrain = CITY
tilemap.regen_cells()
tilemap.update_reachable()
astar = AStar(tilemap.width, tilemap.height)
route = astar.solve(tilemap.player_start, tilemap.player_goal, tilemap.cells)
tilemap.display_route(route)


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
	HILL: pygame.image.load('10hills.png'),
	GRASS: pygame.image.load('10grass.png'),
	WATER: pygame.image.load('10water.png'),
	FOREST: pygame.image.load('10forest.png'),
	COAST: pygame.image.load('10coast.png'),
	CITY: pygame.image.load('10city.png'),
	LOWHILL: pygame.image.load('10lowhills.png'),
	MOUNTAIN: pygame.image.load('10mountain.png')
}

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*(TILESIZE), MAPHEIGHT*(TILESIZE) + 100))
PLAYER = pygame.image.load('10player.png').convert_alpha()
playerPos = tilemap.player_start
fps_clock = pygame.time.Clock()
fps_clock.tick(24)
DISPLAYSURF.fill(BLACK)

INVFONT = pygame.font.Font('FreeSansBold.ttf', 18)

GATHER = 10
TERRAFORM = 100

print len(tilemap._map)
print len(tilemap._map[0])

path = route
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
	if len(path) == 1:
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
