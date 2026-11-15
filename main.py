import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 640))
print("Window Loaded")
pygame.display.set_caption("Hackopoly")
print("Window Title Made")
clock = pygame.time.Clock()

running = True
while running:
    # Event Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game Statements
    # Player code and other loops

    # Change screen color
    screen.fill((30, 30, 30))


    # Update screen and force 60 fps cap
    pygame.display.flip()
    clock.tick(60)

# Close Everything
pygame.quit()
sys.exit()