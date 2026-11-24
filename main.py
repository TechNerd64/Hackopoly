
import pygame
import cairosvg
import sys
import io

pygame.init()
screen = pygame.display.set_mode((800, 800))
scale = 0.5
render_scale = 3.5
corner_width = int(150 * scale)
corner_height = corner_width
board_size = int(900 * scale)
tiles_per_side = 6
tile_width = int((board_size - 2 * corner_width) / tiles_per_side)
tile_height = int(150 * scale)
board_roation = 0

def prepare_corner(corner_name):
    svg_data = cairosvg.svg2png(
        url=f"assets/corners/{corner_name}.svg",
        output_width=int(corner_width * render_scale),
        output_height=int(corner_height * render_scale)
    )

    high_res_tile = pygame.image.load(
        io.BytesIO(svg_data)
    ).convert_alpha()

    corner_image = pygame.transform.smoothscale(
        high_res_tile,
        (corner_width, corner_height)
    )

    return corner_image


def prepare_tile(tile_name):
    svg_data = cairosvg.svg2png(
        url=f"assets/tiles/{tile_name}.svg",
        output_width=int(tile_width * render_scale),
        output_height=int(tile_height * render_scale)
    )

    high_res_tile = pygame.image.load(
        io.BytesIO(svg_data)
    ).convert_alpha()

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

    # Load rotated tiles
    bottom_tile = property_image
    top_tile = pygame.transform.rotate(property_image, 180)
    left_tile = pygame.transform.rotate(property_image, -90)
    right_tile = pygame.transform.rotate(property_image, 90)

    # Top and Bottom
    for i in range(tiles_per_side):
        x = corner_width + i * tile_width

        screen.blit(top_tile, (x, 0))
        screen.blit(bottom_tile, (x, board_size - corner_height))

    # Left and Right sides
    for i in range(tiles_per_side):
        y = corner_height + i * tile_width

        screen.blit(left_tile, (0, y))
        screen.blit(right_tile, (board_size - corner_width, y))

    # Corners
    screen.blit(corner_image, (0, 0))
    screen.blit(corner_image, (board_size - corner_width, 0))
    screen.blit(corner_image, (0, board_size - corner_height))
    screen.blit(corner_image, (board_size - corner_width, board_size - corner_height))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    load_board()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
