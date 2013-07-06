# Acornus, a game for MolyJam Deux (2013)
# "We're taking acorns to the next level." - Peter Molyneux
#
# main.py - main loop and game essentials
# 

import pygame, os, sys
import settings
import random
from pygame.locals import *

class Game:

	def __init__(self, window):
		self.window = window
		self.tree = OakTree(None)
		self.squirrel = Squirrel(None)
		self.accum_time = 0.0
		self.total_time = 0.0


	def update(self, dt):
		e = pygame.event.poll()
	
		if e.type == KEYUP:
			self.squirrel.update(dt, e.key)
		elif e.type == QUIT:
			close()
		
		self.accum_time += dt
		self.total_time += dt
				
		period = settings.SPAWN_PERIOD - \
			(settings.SPAWN_PERIOD - settings.SPAWN_PERIOD_END) * \
			(self.total_time / settings.SPAWN_SCALE_TIME)

		period = min(period, settings.SPAWN_PERIOD_END)


		if int(self.accum_time) >= period:
			#generate branches
			self.tree.generate()
			self.accum_time = 0.0
	
	def draw(self):
		pass

class Squirrel():

	def __init__(self, sprite):
		self.nut = 0
		self.sprite = sprite
		self.node = None
		
	def update(self, dt, key):
		
		if key == UP:
		
		elif key == LEFT:
			self.move_to(self.node.left)
		elif key == RIGHT:
			self.move_to(self.node.right)
		elif key == DOWN:
			self.move_to(self.node.parent)
		elif key == SPACE:
		
		
	def move_to(self, target)
		self.node.squirrel = None
		self.node = target
		self.node.squirrel = self

	def draw(self, window, x, y):
		pass

class OakTree():

	def __init__(self, sprite):
		self.sprite = sprite
		self.root = Node()
		self.lean_rate = 0.0
		self.lean = 0.0

	def update(self, dt):
		self.lean += self.lean_rate * dt

	def draw(self, window):
		pass
	
	def leaves(self):
		leaflist = []
		self.root.leaves(leaflist)
		return leaflist

	def generate(self):
		leaves = self.leaves()
		newleaves = []

		for l in leaves:
			l.left = Node(l)
			l.right = Node(l)	
			l.nut = 0
			newleaves.append(l.left)
			newleaves.append(l.right)

		acorns = len(leaves) / 2

		while(acorns > 0):
			i = random.randrange(len(newleaves))
			
			if newleaves[i].nut == 0:	
				newleaves[i].grow_nut()
				acorns -= 1
		

	#Determines weight on two main subtrees, updates
	def balance(self):
		if self.root.left and self.root.right:
			weight_left = self.root.left.weight()		
			weight_right = self.root.right.weight()
			
			weight_diff = weight_right - weight_left
			self.lean_rate = weight_diff * settings.LEAN_RATE_SCALE

class Node:
	
	def __init__(self, parent = None):
		self.parent = parent or self
		self.left = None
		self.right = None
		self.nut = 0
		self.squirrel = None

	def grow_nut(self):
		if self.nut == 0: #if selected for growth and no acorn present, generate one of random weight
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
	
	#returns leaves for this subtree
	def leaves(self, leaflist):
		if not (self.left or self.right):
			leaflist.append(self)
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
