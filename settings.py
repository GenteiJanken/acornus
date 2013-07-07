import pygame
# Period of tree branching (secs)
GROWTH_PERIOD = 30
GROWTH_SCALE_TIME = 10
GROWTH_PERIOD_END = 90

# Tree dimensions
TRUNK_DIMENSIONS = (50, 100)
TRUNK_ROTATION = 90
BRANCH_LENGTH = 0.18
BRANCH_LENGTH_SCALE = 0.75
BRANCH_ROTATION = 45.0 #degrees
BRANCH_ROTATION_SCALE = 0.8


# Tree leaning (degrees)
LEAN_RATE_SCALE = 2.5
LEAN_THRESHOLD = 100.0

#Colours
SKY_COLOUR = (135, 206, 250) # sky blue
BRANCH_COLOUR = (73, 54, 33) # cafe noir
TEXT_COLOUR = (0, 0 , 0)
DANGER_COLOUR = (255, 0, 0)

#Images
IMG_SQUIRREL = pygame.image.load('img/squirrel.png')

IMG_ACORNS = (
	pygame.image.load('img/acorn_bronze.png'), 
	pygame.image.load('img/acorn_silver.png'), 
	pygame.image.load('img/acorn_gold.png')
)
# Other
MAX_GENERATIONS = 5
