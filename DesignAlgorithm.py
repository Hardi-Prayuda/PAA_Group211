import pygame
import random
import time
import threading

# Inisialisasi Pygame
pygame.init()
# Ukuran layar
screen_width = 1000
screen_height = 650

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (245, 5, 9)
MAROON=(28, 59, 34)
BLUE = (50, 157, 168)
PINK = (21, 76, 77)
YELLOW = (255, 137, 3)
ORANGE=(245, 167, 78)

# Ukuran sel dalam labirin
cell_size = 20
cell_width = (screen_width - 300) // cell_size
cell_height = screen_height // cell_size

# Jarak pandang Droid Hijau
green_droid_visibility = 1

red_droids_count = 0
red_droid_row = None
red_droid_col = None

# Inisialisasi layar
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DESIGN AND ANLYSIS ALGORITHM")

# Membuat grid labirin
maze = []
for i in range(cell_height):
    maze.append([1] * cell_width)

# Fungsi untuk mengacak posisi tembok
def randomize_maze(row, col):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        new_row = row + dx
        new_col = col + dy

        if new_row < 0 or new_row >= cell_height or new_col < 0 or new_col >= cell_width:
            continue

        if maze[new_row][new_col] == 1:
            maze[new_row][new_col] = 0
            maze[row + dx // 2][col + dy // 2] = 0
            randomize_maze(new_row, new_col)

# Fungsi untuk memastikan semua jalur terhubung satu sama lain
def connect_maze(row, col):
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        new_row = row + dx
        new_col = col + dy

        if new_row < 0 or new_row >= cell_height or new_col < 0 or new_col >= cell_width:
            continue

        if maze[new_row][new_col] == 1:
            maze[new_row][new_col] = 0
            maze[row + dx // 2][col + dy // 2] = 0
            connect_maze(new_row, new_col)

#fungsi untuk menggambar labirin
def draw_maze():
    for row in range(cell_height):
        for col in range(cell_width):
            if pov_red:
                # Jika POV Droid Merah aktif, gambar sel labirin secara normal (tanpa memperhatikan droid hijau)
                if maze[row][col] == 1 and not (row == green_droid_row and col == green_droid_col):
                    pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))
            elif pov_green:
                # Jika POV Droid Hijau aktif, gambar sel labirin hanya di sekitar droid hijau
                if abs(row - green_droid_row) <= green_droid_visibility and abs(col - green_droid_col) <= green_droid_visibility:
                    if maze[row][col] == 1 and not (row == green_droid_row and col == green_droid_col):
                        pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size))
                    else:
                        pygame.draw.rect(screen, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))
                    # Menggambar droid hijau
                    if row == green_droid_row and col == green_droid_col:
                        draw_droid(GREEN, row, col)
            else:
                # Jika POV Droid tidak aktif, gambar sel labirin secara normal
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))