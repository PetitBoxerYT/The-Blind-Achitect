import os
import random
import sys
import msvcrt
import time

WIDTH = 40
HEIGHT = 20
ENEMY_COUNT = 5
TICK_RATE = 0.2  # secondes entre chaque tick

def clear():
    os.system("cls")

def generate_map():
    grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if random.random() < 0.12:
                row.append("#")
            else:
                row.append(".")
        grid.append(row)
    return grid

def spawn_enemies(grid, player_x, player_y):
    enemies = []
    while len(enemies) < ENEMY_COUNT:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)
        if grid[y][x] == "." and not (x == player_x and y == player_y):
            enemies.append([x, y])
    return enemies

def print_map(grid, player_x, player_y, enemies):
    clear()
    for y in range(HEIGHT):
        line = ""
        for x in range(WIDTH):
            if x == player_x and y == player_y:
                line += "@"
            elif [x, y] in enemies:
                line += "E"
            else:
                line += grid[y][x]
        print(line)

def get_input_non_blocking():
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b"z":
            return (0, -1)
        if key == b"s":
            return (0, 1)
        if key == b"q":
            return (-1, 0)
        if key == b"d":
            return (1, 0)
        if key == b"\x1b":  # ESC
            sys.exit()
    return (0, 0)

def move_enemies(enemies, player_x, player_y, grid):
    for e in enemies:
        dx = 1 if player_x > e[0] else -1 if player_x < e[0] else 0
        dy = 1 if player_y > e[1] else -1 if player_y < e[1] else 0

        new_x = e[0] + dx
        new_y = e[1] + dy

        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            if grid[new_y][new_x] != "#":
                e[0] = new_x
                e[1] = new_y

def main():
    while True:
        grid = generate_map()
        player_x = WIDTH // 2
        player_y = HEIGHT // 2
        enemies = spawn_enemies(grid, player_x, player_y)

        while True:
            print_map(grid, player_x, player_y, enemies)

            if [player_x, player_y] in enemies:
                print("\nGAME OVER — Press any key to restart.")
                msvcrt.getch()
                break

            dx, dy = get_input_non_blocking()
            new_x = player_x + dx
            new_y = player_y + dy

            if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
                if grid[new_y][new_x] != "#":
                    player_x = new_x
                    player_y = new_y

            move_enemies(enemies, player_x, player_y, grid)

            time.sleep(TICK_RATE)

if __name__ == "__main__":
    main()
