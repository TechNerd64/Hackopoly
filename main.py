import ctypes
import os

if os.name == "nt":
    _cairo_dll_dir = r"C:\Program Files\GTK3-Runtime Win64\bin"
    _dll_directory_handle = os.add_dll_directory(_cairo_dll_dir)
    _cairo_dll = ctypes.CDLL(os.path.join(_cairo_dll_dir, "libcairo-2.dll"))

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

corner_width = 150
corner_height = 150
tile_width = 103
tile_height = 150
tiles_per_side = 9
board_size = 2 * corner_width + tiles_per_side * tile_width
render_scale = 3
scale = 0.75
background_color = (30, 30, 30)


def prepare_corner(corner_name):
    svg_path = f"assets/corners/{corner_name}.svg"

    png_data = cairosvg.svg2png(
        url=svg_path,
        output_width=corner_width * render_scale,
        output_height=corner_height * render_scale,
    )

    image = pygame.image.load(io.BytesIO(png_data)).convert_alpha()
    image = pygame.transform.smoothscale(image, (corner_width, corner_height))
    return image


def prepare_tile(tile_name):
    svg_path = f"assets/tiles/{tile_name}.svg"

    png_data = cairosvg.svg2png(
        url=svg_path,
        output_width=tile_width * render_scale,
        output_height=tile_height * render_scale,
    )

    image = pygame.image.load(io.BytesIO(png_data)).convert_alpha()

    image = pygame.transform.smoothscale(image, (tile_width, tile_height))

    return image


def load_board():
    board_surface = pygame.Surface((board_size, board_size), pygame.SRCALPHA)

    corner_image = prepare_corner("GO")
    tile_image = prepare_tile("scratch-tile")

    top_y = 0
    bottom_y = board_size - corner_height

    left_x = 0
    right_x = board_size - corner_width

    for i in range(tiles_per_side):
        x = corner_width + i * tile_width
        y = corner_height + i * tile_width

        bottom_tile = tile_image
        top_tile = pygame.transform.rotate(tile_image, 180)
        right_tile = pygame.transform.rotate(tile_image, 90)
        left_tile = pygame.transform.rotate(tile_image, -90)

        board_surface.blit(top_tile, (x, top_y))
        board_surface.blit(bottom_tile, (x, bottom_y))
        board_surface.blit(left_tile, (left_x, y))
        board_surface.blit(right_tile, (right_x, y))

    board_surface.blit(pygame.transform.rotate(corner_image, 180), (0, 0))
    board_surface.blit(
        pygame.transform.rotate(corner_image, 90), (board_size - corner_width, 0)
    )
    board_surface.blit(
        pygame.transform.rotate(corner_image, 270), (0, board_size - corner_height)
    )
    board_surface.blit(
        pygame.transform.rotate(corner_image, 0),
        (board_size - corner_width, board_size - corner_height),
    )
    return board_surface


board_surface = load_board()

scaled_board_size = round(board_size * scale)

scaled_board = pygame.transform.smoothscale(
    board_surface, (scaled_board_size, scaled_board_size)
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
