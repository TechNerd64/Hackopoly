import pygame
import cairosvg
import io
import sys

pygame.init()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hackopoly")
clock = pygame.time.Clock()

scale = 0.5
board_size = 1800
corner_width = 300
corner_height = 300
tiles_per_side = 9
tile_height = 200
tile_width = int((board_size - 2 * corner_width) / tiles_per_side)
render_scale = 3
background_color = (30, 30, 30)


def prepare_corner(corner_name):
    svg_path = f"assets/corners/{corner_name}.svg"

    png_data = cairosvg.svg2png(
        url=svg_path,
        output_width=corner_width * render_scale,
        output_height=corner_height * render_scale
    )

    image = pygame.image.load(io.BytesIO(png_data)).convert_alpha()

    image = pygame.transform.smoothscale(
        image,
        (corner_width, corner_height)
    )

    return image


def prepare_tile(tile_name):
    svg_path = f"assets/tiles/{tile_name}.svg"

    png_data = cairosvg.svg2png(
        url=svg_path,
        output_width=int(tile_width * render_scale),
        output_height=tile_height * render_scale
    )

    image = pygame.image.load(io.BytesIO(png_data)).convert_alpha()

    image = pygame.transform.smoothscale(
        image,
        (round(tile_width), tile_height)
    )

    return image


def load_board():
    board_surface = pygame.Surface(
        (board_size, board_size),
        pygame.SRCALPHA
    )

    corner_image = prepare_corner("GO")
    tile_image = prepare_tile("scratch-tile")

    tile_depth_offset = (corner_height - tile_height) // 2

    top_y = tile_depth_offset
    bottom_y = board_size - corner_height + tile_depth_offset

    left_x = tile_depth_offset
    right_x = board_size - corner_width + tile_depth_offset

    for i in range(tiles_per_side):
        x1 = corner_width + round(i * (board_size - 2 * corner_width) / tiles_per_side)
        x2 = corner_width + round((i + 1) * (board_size - 2 * corner_width) / tiles_per_side)

        current_width = x2 - x1

        tile = pygame.transform.smoothscale(
            tile_image,
            (current_width, tile_height)
        )

        board_surface.blit(tile, (x1, top_y))

        bottom_tile = pygame.transform.rotate(tile, 180)

        board_surface.blit(bottom_tile, (x1, bottom_y))

    for i in range(tiles_per_side):
        y1 = corner_height + round(i * (board_size - 2 * corner_height) / tiles_per_side)
        y2 = corner_height + round((i + 1) * (board_size - 2 * corner_height) / tiles_per_side)

        current_height = y2 - y1

        tile = pygame.transform.smoothscale(
            tile_image,
            (current_height, tile_height)
        )

        left_tile = pygame.transform.rotate(tile, 90)
        right_tile = pygame.transform.rotate(tile, -90)

        board_surface.blit(left_tile, (left_x, y1))
        board_surface.blit(right_tile, (right_x, y1))

    board_surface.blit(corner_image, (0, 0))
    board_surface.blit(corner_image, (board_size - corner_width, 0))
    board_surface.blit(corner_image, (0, board_size - corner_height))
    board_surface.blit(
        corner_image,
        (board_size - corner_width, board_size - corner_height)
    )

    return board_surface


board_surface = load_board()

scaled_board_size = int(board_size * scale)

scaled_board = pygame.transform.smoothscale(
    board_surface,
    (scaled_board_size, scaled_board_size)
)

board_x = (screen_width - scaled_board_size) // 2
board_y = (screen_height - scaled_board_size) // 2


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    screen.blit(scaled_board, (board_x, board_y))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()