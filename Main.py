import pygame

pygame.init()
color = (255,255,255)
position = (0,0)
CANVAS = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("Ernst Games")
running = True

while running:
    CANVAS.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
