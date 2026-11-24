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
corner_width = int(150 * scale)
corner_height = corner_width
board_size = int(900 * scale)
board_roation = 0

def prepare_corner(corner_name):
      ## Convert SVG to PNG in memory
        svg_data = cairosvg.svg2png(
            url= f"assets/corners/{corner_name}.svg",
            output_width = corner_width * render_scale,
            output_height = corner_height * render_scale
        )
        high_res_tile = pygame.image.load(io.BytesIO(svg_data)).convert_alpha()
        corner_image = pygame.transform.smoothscale(
            high_res_tile,
            (corner_width, corner_height)
        )
        return corner_image
    

def prepare_tile(tile_name):
    ## Convert SVG to PNG in memory
    svg_data = cairosvg.svg2png(
        url= f"assets/tiles/{tile_name}.svg",
        output_width = tile_width * render_scale,
        output_height = tile_height * render_scale
    )
    high_res_tile = pygame.image.load(io.BytesIO(svg_data)).convert_alpha()
    tile_image = pygame.transform.smoothscale(
        high_res_tile,
        (tile_width, tile_height)
    )
    return tile_image

pygame.display.set_caption("Hackopoly")
clock = pygame.time.Clock()


def load_board():
    corner_image = prepare_corner("GO")
    property_image = prepare_tile("scratch-tile")
    # Load Rotated Tiles
    bottom_tile = property_image
    top_tile = pygame.transform.rotate(property_image, 180)
    left_tile = pygame.transform.rotate(property_image, -90)
    right_tile = pygame.transform.rotate(property_image, 90)


    # Top and Bottom
    for x in range(0, board_size, tile_width):
        screen.blit(top_tile, (x, 0))
        screen.blit(bottom_tile, (x, (board_size - tile_height)+int(150 * scale)))

    # Left and Right sides
    for y in range(0, board_size, tile_width):
        screen.blit(left_tile, (0,y))
        screen.blit(right_tile, (board_size - tile_height, y))
        

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

