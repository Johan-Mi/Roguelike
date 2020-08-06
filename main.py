#!/usr/bin/env python3
"""This module lets you play a roguelike dungeon crawler."""

import math
from PIL import Image
from gfx.brick import *

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360

FOV = 3.1
RAY_STEP = 0.015

TILE_TEXTURE_WIDTH = 32
TILE_TEXTURE_HEIGHT = 48

player_x = 1
player_y = 1
player_dir = 1

game_map = None
map_width = None
map_height = None

with open("game/map.txt") as map_file:
    game_map = [row[:-1] for row in map_file.readlines()]
map_width = len(game_map[0])
map_height = len(game_map)


def start():
    global player_x, player_y, player_dir
    player_x = 1
    player_y = 1
    player_dir = 1


def update(key):
    global player_x, player_y, player_dir
    key = key.lower()
    if key in ("w", "a", "s", "d", "start"):
        if key == "w":
            if player_dir == 0:
                if game_map[player_y][player_x + 1] == " ":
                    player_x += 1
            elif player_dir == 1:
                if game_map[player_y + 1][player_x] == " ":
                    player_y += 1
            elif player_dir == 2:
                if game_map[player_y][player_x - 1] == " ":
                    player_x -= 1
            elif player_dir == 3:
                if game_map[player_y - 1][player_x] == " ":
                    player_y -= 1
        elif key == "s":
            if player_dir == 0:
                if game_map[player_y][player_x - 1] == " ":
                    player_x -= 1
            elif player_dir == 1:
                if game_map[player_y - 1][player_x] == " ":
                    player_y -= 1
            elif player_dir == 2:
                if game_map[player_y][player_x + 1] == " ":
                    player_x += 1
            elif player_dir == 3:
                if game_map[player_y + 1][player_x] == " ":
                    player_y += 1
        elif key == "d":
            player_dir += 1
            if player_dir == 4:
                player_dir = 0
        elif key == "a":
            player_dir -= 1
            if player_dir == -1:
                player_dir = 3
        elif key == "start":
            start()

        redraw()


def redraw():
    screen = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT),
                       (0x0e, 0x0e, 0x0e))

    for ray_num in range(SCREEN_WIDTH):
        ray_dir = (player_dir * math.pi * 0.5 + math.atan(
            (ray_num / SCREEN_WIDTH - 0.5) * FOV)) % (math.pi * 2)
        eye_x = math.cos(ray_dir)
        eye_y = math.sin(ray_dir)

        ray_x = player_x + 0.5
        ray_y = player_y + 0.5

        if math.pi * 1.5 > ray_dir > math.pi * 0.5:  # Left grid line
            ray_vert_dist = abs(ray_x % 1 / math.cos(ray_dir))
        else:  # Right grid line
            ray_vert_dist = abs((ray_x % 1 - 1) / math.cos(ray_dir))

        if ray_dir > math.pi:  # Top grid line
            ray_horiz_dist = abs(ray_y % 1 / math.cos(math.pi * 0.5 - ray_dir))
        else:  # Bottom grid line
            ray_horiz_dist = abs(
                (ray_y % 1 - 1) / math.cos(math.pi * 0.5 - ray_dir))

        ray_dist = min(ray_horiz_dist, ray_vert_dist)

        while game_map[int(player_y + 0.5 +
                           eye_y * ray_dist)][int(player_x + 0.5 +
                                                  eye_x * ray_dist)] != "#":
            ray_dist += RAY_STEP

        ray_dist_adjusted = ray_dist * math.cos(player_dir * math.pi * 0.5 -
                                                ray_dir)

        wall_height = int(SCREEN_HEIGHT / ray_dist_adjusted * 0.45)

        ray_x = player_x + 0.5 + eye_x * ray_dist
        ray_y = player_y + 0.5 + eye_y * ray_dist

        ray_x_prev = ray_x - eye_x * RAY_STEP
        ray_y_prev = ray_y - eye_y * RAY_STEP

        if (int(ray_x) != int(ray_x_prev)):
            texture_x = int((ray_y % 1) * TILE_TEXTURE_WIDTH)
        else:
            texture_x = int((ray_x % 1) * TILE_TEXTURE_WIDTH)

        for y_pos in range(
                max((wall_height - SCREEN_HEIGHT) // 2, 0),
                min(SCREEN_HEIGHT - ((SCREEN_HEIGHT - wall_height) // 2),
                    wall_height)):
            texture_y = int(y_pos / wall_height * TILE_TEXTURE_HEIGHT)
            color = BRICK_TEXTURE[texture_y * TILE_TEXTURE_WIDTH + texture_x]
            shading = math.exp(-math.sqrt(ray_dist / 2))
            color = tuple(int(i * shading) for i in color)
            screen.putpixel(
                (ray_num, ((SCREEN_HEIGHT - wall_height) // 2) + y_pos), color)

    for y_pos in range(map_height):
        for x_pos in range(map_width):
            color = {
                "#": (0xbb, 0xc2, 0xcf),
                " ": (0x02, 0x02, 0x02),
            }[game_map[y_pos][x_pos]]
            screen.putpixel((x_pos * 2 + 3, y_pos * 2 + 3), color)
            screen.putpixel((x_pos * 2 + 3, y_pos * 2 + 4), color)
            screen.putpixel((x_pos * 2 + 4, y_pos * 2 + 3), color)
            screen.putpixel((x_pos * 2 + 4, y_pos * 2 + 4), color)
    screen.putpixel((player_x * 2 + 3, player_y * 2 + 3), (0xff, 0x00, 0x00))
    screen.putpixel((player_x * 2 + 3, player_y * 2 + 4), (0xff, 0x00, 0x00))
    screen.putpixel((player_x * 2 + 4, player_y * 2 + 3), (0xff, 0x00, 0x00))
    screen.putpixel((player_x * 2 + 4, player_y * 2 + 4), (0xff, 0x00, 0x00))

    screen.save("game/img.png")


def main():
    """Starts the game."""
    start()
    redraw()
    while True:
        update(input("> "))


if __name__ == "__main__":
    main()
