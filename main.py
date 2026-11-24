import pygame
import cairosvg
import sys
import io

pygame.init()
screen = pygame.display.set_mode((800, 800))
scale = 0.5
render_scale = 3.5
tile_width = int(103 * scale)
tile_height = int(150 * scale)
board_size = int(900 * scale)

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

pygame.display.set_caption("Hackopoly")
clock = pygame.time.Clock()


def load_board():
    rotation = 0
    for i in range(4):
        rotation += 1
        for x in range(0, board_size, tile_width):
            screen.blit(property_image, (x, 0))
        

running = True
while running:
    # Event Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render blank background
    screen.fill((30, 30, 30))
    
    # Game Loop
    load_board()

    # Update screen and force 60 fps cap
    pygame.display.flip()
    clock.tick(60)

# Close Everything
pygame.quit()
sys.exit()

