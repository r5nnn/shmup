import pygame

# whole project initialised
pygame.init()

# window parameters
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800

# initialise game assets
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
hitbox = pygame.Rect((300, 400, 10, 10))
pygame.display.set_caption('shmup alpha 0.0.0')
icon = pygame.image.load('assets\icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# start gameloop
run = True
while run:
    # update screen
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), hitbox)
    # key & screen border detection
    key = pygame.key.get_pressed()
    if hitbox.top > 0 and key[pygame.K_w]:
        hitbox.move_ip(0, -4)
    if hitbox.left > 0 and key[pygame.K_a]:
        hitbox.move_ip(-4, 0)
    if hitbox.bottom < SCREEN_HEIGHT and key[pygame.K_s]:
        hitbox.move_ip(0, 4)
    if hitbox.right < SCREEN_WIDTH and key[pygame.K_d]:
        hitbox.move_ip(4, 0)
    for event in pygame.event.get():
        # exit out method
        if event.type == pygame.QUIT:
            run = False
    # update the game every 60 ticks (caps game at 60fps)
    pygame.display.flip()
    clock.tick(60)

# game interrupt
pygame.quit()
