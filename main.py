# Gold Acorn, a game for MolyJam Deux (2013)
# "We're taking acorns to the next level." - Peter Molyneux
#
# main.py - main loop and game essentials
# 

import pygame, os, sys
import settings
from pygame.locals import *


pygame.init()

clock = pygame.time.Clock()
running = True

def close():
	global running
	running = False

accum_time = 0.0
total_time = 0.0

while running:
	clock.tick(30)
	dtime = clock.get_time()/1000.0

	accum_time += dtime
	total_time += dtime

	period = 10
	
	if int(accum_time) >= period:
		#generate branches
		accum_time = 0.0

class Entity:

	def __init__(self):
		pass	
	
	def update(self, dt):
		pass

	def draw(self):
		pass


class Squirrel(Entity):

	def __init__(self):
		self.nut = 0
	
	def update(self, dt):
		pass

	def draw(self):
		pass

class OakTree(Entity):

	def __init__(self):
		self.root = Node()
		self.lean = 0
	
	def draw(self):
		pass


	def generate(self):
		pass

	def balance(self):
		pass	

class Node:
	
	def __init__(self, parent = None):
		self.parent = parent or self
		self.left = None
		self.right = None
		self.nut = 0

	def grow_nut(self):
		pass
