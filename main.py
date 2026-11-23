import pygame
import cairosvg
import sys
import io

pygame.init()
screen = pygame.display.set_mode((800, 800))
scale = 0.75
render_scale = 4
tile_width = 103 * scale
tile_height = 150 * scale

## Convert SVG to PNG in memory
svg_data = cairosvg.svg2png(
    url="assets/scratch-tile.svg",
    output_width = tile_width * render_scale,
    output_height = tile_height * render_scale
)

high_res_tile = pygame.image.load(io.BytesIO(svg_data)).convert_alpha()
property_image = pygame.transform.smoothscale(
    high_res_tile,
    (tile_width, tile_height)
)

property_image = pygame.transform.scale(property_image, (103 * scale, 150 * scale))

pygame.display.set_caption("Hackopoly")
clock = pygame.time.Clock()

running = True
while running:
    # Event Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Change screen color
    screen.fill((30, 30, 30))
    for x in range(0, 800, int(103 * scale)):
        screen.blit(property_image, (x, 0))

    # Update screen and force 60 fps cap
    pygame.display.flip()
    clock.tick(60)

# Close Everything
pygame.quit()
sys.exit()