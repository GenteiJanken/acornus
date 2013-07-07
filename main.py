# Acornus, a game for MolyJam Deux (2013) by Josh Douglass-Molloy, with illustrations by Colin Capurso
# "We're taking acorns to the next level." - Peter Molyneux
#
# main.py - main loop and game essentials
# 

import pygame, os, sys
import settings
import random, math
from pygame.locals import *

class Game:

	def __init__(self, window):
		self.window = window
		self.tree = OakTree()
		self.squirrel = Squirrel(self.tree)
		self.tree.generate()
		
		self.accum_time = 0.0
		self.total_time = 0.0
		

	def update(self, dt):
		e = pygame.event.poll()
	
		if e.type == KEYUP:
			self.squirrel.update(dt, e.key)
		elif e.type == VIDEORESIZE:
			self.window = pygame.display.set_mode((e.size), pygame.RESIZABLE)
		elif e.type == QUIT:
			close()
		
		self.accum_time += dt
		self.total_time += dt
					
		period = settings.GROWTH_PERIOD - \
			(settings.GROWTH_PERIOD - settings.GROWTH_PERIOD_END) * \
			(self.total_time / settings.GROWTH_SCALE_TIME)

		period = min(period, settings.GROWTH_PERIOD_END)
		
		if int(self.accum_time) >= period and self.tree.generations < settings.MAX_GENERATIONS:
			#generate branches
			self.tree.generate()
			self.accum_time = 0.0
			

	def draw(self):
		self.window.fill(settings.SKY_COLOUR)
		self.tree.draw(self.window)
		self.squirrel.draw(self.window)
		pygame.display.update()

	def world_to_screen(x, y):
		pass

class Squirrel():

	def __init__(self, tree):
		self.nut = 0
		self.sprite = settings.IMG_SQUIRREL
		self.tree = tree
		self.node = tree.root
		
	def update(self, dt, key):
		
		if key == K_UP:
	
			if self.node.nut == 0:
				self.node.nut = self.nut
				self.nut = 0
			else:
				tmp = self.nut
				self.nut = self.node.nut 
				self.node.nut = tmp	
			
			self.tree.balance()					
	
		elif key == K_LEFT and self.node.left:
			self.move_to(self.node.left)
		elif key == K_RIGHT and self.node.right:
			self.move_to(self.node.right)
		elif key == K_DOWN and not (self.node.parent == self.node):
			self.move_to(self.node.parent)
	

	def move_to(self, target):
		self.node.squirrel = None
		self.node = target
		self.node.squirrel = self

	def draw(self, window):
		x = self.node.position[0]
		y = self.node.position[1]
		
		flip = (self.node == self.node.parent.left)
		window.blit(pygame.transform.flip(pygame.transform.scale(self.sprite, (32, 32)), flip, False), self.node.position)

class OakTree():

	def __init__(self):
			
		self.lean_rate = 0.0
		self.lean = 0.0
		self.dimensions = [settings.TRUNK_DIMENSIONS[0], settings.TRUNK_DIMENSIONS[1]]		
		self.root = Node(settings.TRUNK_ROTATION, (500, 100))
		self.generations = 0

	def update(self, dt):
		self.lean += self.lean_rate * dt
		return self.lean

	def draw(self, window):		  
		self.root.draw(window)
	
	def leaves(self):
		leaflist = []
		self.root.leaves(leaflist)
		return leaflist

	def generate(self):
		leaves = self.leaves()
		newleaves = []

		for l in leaves:
			leftrot = l.rotation + settings.BRANCH_ROTATION
			leftpos = (l.position[0] + settings.BRANCH_LENGTH * math.cos(math.radians(leftrot)), l.position[1] + settings.BRANCH_LENGTH * math.sin(math.radians(leftrot)))
			
			rightrot = l.rotation - settings.BRANCH_ROTATION
			rightpos = (l.position[0] + settings.BRANCH_LENGTH * math.cos(math.radians(rightrot)), l.position[1] + settings.BRANCH_LENGTH * math.sin(math.radians(rightrot)))

			l.left = Node(leftrot, leftpos, l)
			l.right = Node(rightrot, rightpos, l)	
			l.nut = 0
			newleaves.append(l.left)
			newleaves.append(l.right)

		acorns = len(newleaves) / 2

		while(acorns > 0):
			i = random.randrange(len(newleaves))
			
			if newleaves[i].nut == 0:	
				newleaves[i].grow_nut()
				acorns -= 1

		settings.BRANCH_LENGTH *= settings.BRANCH_LENGTH_SCALE
		settings.BRANCH_ROTATION *= settings.BRANCH_ROTATION_SCALE		
		self.generations += 1
		self.balance()

	#Determines weight on two main subtrees, updates
	def balance(self):
		if self.root.left and self.root.right:
			weight_left = self.root.left.weight()		
			weight_right = self.root.right.weight()
			
			weight_diff = weight_right - weight_left
			self.lean_rate = weight_diff * settings.LEAN_RATE_SCALE

class Node:
	
	def __init__(self, rotation, position, parent = None):
		self.parent = parent or self
		self.left = None
		self.right = None
		self.position = position
		self.rotation = rotation
		self.nut = 0
		self.squirrel = None

	def grow_nut(self):
		self.nut = random.randint(1, 3)

	def weight(self):
		if not (self.left or self.right):
			return 1 + self.nut
		else:
			return 1 + self.nut + self.left.weight() + self.right.weight()

	def depth(self):
		if self.parent == self:
			return 0
		else:
			return 1 + self.parent.depth()
	
	def draw(self, window):

		if self.nut > 0:
			window.blit(pygame.transform.scale(settings.IMG_ACORNS[self.nut-1], (16, 16)), self.position)

		if not (self.left or self.right):
			return
		else:
		
			pygame.draw.line(window, settings.BRANCH_COLOUR, self.position, self.left.position, 8)
			pygame.draw.line(window, settings.BRANCH_COLOUR, self.position, self.right.position, 8)
			self.left.draw(window)
			self.right.draw(window)

	#returns leaves for this subtree
	def leaves(self, leaflist):
		if not (self.left or self.right):
			leaflist.append(self)
			return
		else:
			self.left.leaves(leaflist)
			self.right.leaves(leaflist)	
	
	

pygame.init()

clock = pygame.time.Clock()
running = True

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
game = Game(window)

def close():
	global running
	running = False

while running:
	clock.tick(30)
	dt = clock.get_time()/1000.0
	game.update(dt)
	game.draw()
