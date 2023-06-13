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
                    
#fungsi untuk menggambar droid
def draw_droid(color, row, col):
    radius = cell_size // 2
    x = col * cell_size + radius
    y = row * cell_size + radius
    pygame.draw.circle(screen, color, (x, y), radius)

#fungsi untuk membuat tampilan menu
def draw_menu_bar():
    pygame.draw.rect(screen, MAROON, (screen_width - 280, 0, 300, screen_height))

    font = pygame.font.Font(None, 35)
    labels = ["MULAI", "ACAK MAP", "ACAK DROID", "POV DROID HIJAU","", "POV DROID MERAH", "TAMBAH DROID", "KURANGI DROID","PAUSE"]
    # Menambahkan tulisan "Menu Permainan"
    judul_font = pygame.font.Font(None, 40)
    judul_text = judul_font.render("MENU GAME", True, WHITE)
    judul_text_rect = judul_text.get_rect(center=(screen_width - 143, 30))
    screen.blit(judul_text, judul_text_rect)
    for i, label in enumerate(labels):
        button_rect = pygame.Rect(screen_width - 260, 50 + i * 50, 240, 40)
        pygame.draw.rect(screen, PINK, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 2)

        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pov_red_button_rect = pygame.Rect(screen_width - 260, 50 + 5 * 50, 240, 40)
    if pov_red:
        pygame.draw.rect(screen, RED, pov_red_button_rect)
    else:
        pygame.draw.rect(screen, PINK, pov_red_button_rect)
    pygame.draw.rect(screen, WHITE, pov_red_button_rect, 2)
    pov_red_text = font.render("", True, WHITE)
    pov_red_text_rect = pov_red_text.get_rect(center=pov_red_button_rect.center)
    screen.blit(pov_red_text, pov_red_text_rect)

    pov_green_button_rect = pygame.Rect(screen_width - 260, 50 + 3 * 50, 240, 40)
    if pov_green:
        pygame.draw.rect(screen, GREEN, pov_green_button_rect)
    else:
        pygame.draw.rect(screen, PINK, pov_green_button_rect)
    pygame.draw.rect(screen, WHITE, pov_green_button_rect, 2)
    pov_green_text = font.render("", True, WHITE)
    pov_green_text_rect = pov_green_text.get_rect(center=pov_green_button_rect.center)
    screen.blit(pov_green_text, pov_green_text_rect)

    # Adjust the text position for each button
    for i, label in enumerate(labels):
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(button_rect.centerx, 50 + i * 50 + 20))
        screen.blit(text, text_rect)

    pov_red_text_rect = pov_red_text.get_rect(center=(pov_red_button_rect.centerx, 50 + 5 * 50 + 20))
    screen.blit(pov_red_text, pov_red_text_rect)

    pov_green_text_rect = pov_green_text.get_rect(center=(pov_green_button_rect.centerx, 50 + 3 * 50 + 20))
    screen.blit(pov_green_text, pov_green_text_rect)

    pygame.draw.rect(screen, PINK, (screen_width - 260, 50 + 4 * 50, 240, 40))
    pygame.draw.rect(screen, WHITE, (screen_width - 260, 50 + 4 * 50, 240, 40), 2)
    pygame.draw.rect(screen, ORANGE, (screen_width - 260, 50 + 4 * 50 + 15, 240, 10))
    slider_pos = screen_width - 170 + int((green_droid_visibility - 2.5) / 3 * 170)
    pygame.draw.circle(screen, YELLOW, (slider_pos, 50 + 4 * 50 + 20), 12)

#fungsi untuk membuat acak droid
def randomize_droid(): 
    global green_droid_row, green_droid_col, red_droid_row, red_droid_col

    while True:
        green_droid_row = random.randint(0, cell_height - 1)
        green_droid_col = random.randint(0, cell_width - 1)
        if maze[green_droid_row][green_droid_col] == 0:
            break

    while True:
        red_droid_row = random.randint(0, cell_height - 1)
        red_droid_col = random.randint(0, cell_width - 1)
        if maze[red_droid_row][red_droid_col] == 0:
            break

#fungsi untuk membuat map random
def randomize_map():
    global maze, pov_green, pov_red

    pov_green = False
    pov_red = False

    maze = []
    for i in range(cell_height):
        maze.append([1] * cell_width)

    randomize_maze(0, 0)
    connect_maze(0, 0)
    randomize_droid()  # Mengacak posisi droid setelah mengacak map
    
#fungsi untuk menggerakkan droid merah
def add_red_droid():
    global maze, red_droids_count

    if maze[red_droid_row][red_droid_col] == 0 and red_droids_count < 5:
        if red_droids_count < 5:
            maze[red_droid_row][red_droid_col] = 1
            red_droids_count += 1  # Menambahkan jumlah droid merah yang ada 