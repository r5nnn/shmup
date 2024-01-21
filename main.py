import pygame

# whole project initialised
pygame.init()

# window parameters
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# initialise game assets
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
hitbox = pygame.Rect((300, 400, 10, 10))

# start gameloop
run = True
while run:
    for event in pygame.event.get():
        # exit out method
        if event.type == pygame.QUIT:
            run = False

# game interrupt
pygame.QUIT()
