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
                    # Draw the green droid
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

    # Sesuaikan posisi teks untuk setiap tombol
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
            red_droids_count += 1  # Menambahkan jumlah droid merah yang ada

maze_rows = 10
maze_cols = 10
MAX_RED_DROIDS = 4
red_droids =[]

# Fungsi untuk menambahkan droid merah
def add_droid():
    global red_droids

    if len(red_droids) >= MAX_RED_DROIDS:
        return

    while True:
        red_droid_row = random.randint(0, cell_height - 1)
        red_droid_col = random.randint(0, cell_width - 1)
        if maze[red_droid_row][red_droid_col] == 0 and (red_droid_row != green_droid_row or red_droid_col != green_droid_col):
            break

    red_droids.append((red_droid_row, red_droid_col))

# Fungsi untuk menggerakkan droid merah tambahan
def move_additional_red_droid(red_droid_index):
    global red_droids, green_droid_row, green_droid_col

    red_droid_found = False  # Menandakan apakah droid merah ditemukan

    while True:
        # Menyimpan posisi awal droid merah
        initial_red_row = red_droids[red_droid_index][0]
        initial_red_col = red_droids[red_droid_index][1]

        path = bfs_search(
            red_droids[red_droid_index][0],
            red_droids[red_droid_index][1],
            green_droid_row,
            green_droid_col,
        )
        if path:
            for step in path:
                red_droids[red_droid_index] = step
                time.sleep(0.2)

                if not pov_red:
                    draw_droid(GREEN, green_droid_row, green_droid_col)
                if not pov_green:
                    draw_droid(GREEN, green_droid_row, green_droid_col)
                for red_droid_pos in red_droids:
                    draw_droid(RED, red_droid_pos[0], red_droid_pos[1])
                draw_menu_bar()
                pygame.display.update()
                draw_maze()
                if stop_red_droid or (
                    red_droids[red_droid_index][0] == green_droid_row
                    and red_droids[red_droid_index][1] == green_droid_col
                ):
                    red_droid_found = True  # Menandakan droid merah ditemukan
                    break

                # Cek apakah posisi droid merah berubah setelah pergerakan
                if (
                    red_droids[red_droid_index][0] != initial_red_row
                    or red_droids[red_droid_index][1] != initial_red_col
                ):
                    break

        if red_droid_found:
            break

        # Jika droid merah tambahan tidak dapat menemukan droid hijau
        if (
            red_droids[red_droid_index][0] == green_droid_row
            and red_droids[red_droid_index][1] == green_droid_col
        ):
            return  # Keluar dari fungsi move_additional_red_droid()

        # Kondisi tambahan untuk menghentikan droid hijau saat droid merah tambahan menemukannya
        if (
            red_droids[red_droid_index][0] == green_droid_row
            and red_droids[red_droid_index][1] == green_droid_col
        ):
            return

# Fungsi untuk mengubah jarak pandang droid hijau
def change_green_droid_visibility(pos):
    global green_droid_visibility

    slider_width = 160
    slider_pos = pos[0] - (screen_width - 180)
    percentage = slider_pos / slider_width
    green_droid_visibility = int(percentage * 4) + 2
    
# Fungsi untuk menggerakkan droid merah
def move_red_droid():
    global red_droid_row, red_droid_col, green_droid_row, green_droid_col, red_droid_moving, green_droid_moving

    green_droid_found = False  # Menandakan apakah droid hijau ditemukan

    while True:
        # Menyimpan posisi awal droid hijau
        initial_green_row = green_droid_row
        initial_green_col = green_droid_col

        path = bfs_search(red_droid_row, red_droid_col, green_droid_row, green_droid_col)
        if path:
            for step in path:
                red_droid_row, red_droid_col = step
                time.sleep(0.2)

                if not pov_red:
                    draw_droid(GREEN, green_droid_row, green_droid_col)
                if not pov_green:
                    draw_droid(GREEN, green_droid_row, green_droid_col)
                for red_droid_pos in red_droids:
                    draw_droid(RED, red_droid_pos[0], red_droid_pos[1])
                draw_droid(RED, red_droid_row, red_droid_col)
                draw_menu_bar()
                move_green_droid()
                pygame.display.update()
                draw_maze()
                if stop_red_droid or (red_droid_row == green_droid_row and red_droid_col == green_droid_col):
                    red_droid_moving = False  # Menghentikan gerakan droid merah
                    green_droid_moving = False  # Menghentikan gerakan droid hijau
                    green_droid_found = True  # Menandakan droid hijau ditemukan
                    break

                # Cek apakah posisi droid hijau berubah setelah pergerakan droid merah
                if green_droid_row != initial_green_row or green_droid_col != initial_green_col:
                    break

        if green_droid_found:
            break

        # Jika droid merah tidak dapat menemukan droid hijau
        if red_droid_row == green_droid_row and red_droid_col == green_droid_col:
            red_droid_moving = False  # Menghentikan gerakan droid merah
            green_droid_moving = False  # Menghentikan gerakan droid hijau
            break

        # Jika droid merah tidak dapat menemukan droid hijau
        if red_droid_row == green_droid_row and red_droid_col == green_droid_col:
            red_droid_moving = False  # Menghentikan gerakan droid merah
            green_droid_moving = False  # Menghentikan gerakan droid hijau
            return  # Keluar dari fungsi move_red_droid()

        # Kondisi tambahan untuk menghentikan droid hijau saat droid merah menemukannya
        if red_droid_row == green_droid_row and red_droid_col == green_droid_col:
            red_droid_moving = False  # Menghentikan gerakan droid merah
            green_droid_moving = False  # Menghentikan gerakan droid hijau
            return

#fungsi untuk menggerakkan droid hijau menggunakan algoritma collision detection
def move_green_droid():
    global green_droid_row, green_droid_col, green_droid_moving, red_droid_row, red_droid_col

    # Periksa apakah droid merah dan hijau memiliki posisi yang sama
    if green_droid_row == red_droid_row and green_droid_col == red_droid_col:
        green_droid_moving = False
        return

    neighbors = get_neighbors(green_droid_row, green_droid_col)

    # Saring gerakan aman yang tidak sesuai dengan posisi droid merah
    safe_moves = [(neighbor_row, neighbor_col) for neighbor_row, neighbor_col in neighbors if
                  maze[neighbor_row][neighbor_col] == 0 and (neighbor_row != red_droid_row or neighbor_col != red_droid_col)]

    # Periksa apakah ada gerakan aman yang tersedia
    if safe_moves:
        green_droid_row, green_droid_col = random.choice(safe_moves)

        # Periksa apakah droid merah dan hijau memiliki posisi yang sama setelah bergerak
        if green_droid_row == red_droid_row and green_droid_col == red_droid_col:
            green_droid_moving = False

#Algoritma bfs untuk droid merah    
def bfs_search(start_row, start_col, target_row, target_col):
    visited = [[False] * cell_width for _ in range(cell_height)]
    queue = [(start_row, start_col, [])]

    while queue:
        row, col, path = queue.pop(0)
        if row == target_row and col == target_col:
            return path

        if not visited[row][col]:
            visited[row][col] = True
            neighbors = get_neighbors(row, col)
            for neighbor_row, neighbor_col in neighbors:
                if not visited[neighbor_row][neighbor_col]:
                    queue.append((neighbor_row, neighbor_col, path + [(neighbor_row, neighbor_col)]))

    return None
#fungsi untuk mendapatkan posisi tetangga-tetangga
def get_neighbors(row, col): 
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dx, dy in directions:
        new_row = row + dx
        new_col = col + dy

        if 0 <= new_row < cell_height and 0 <= new_col < cell_width and maze[new_row][new_col] == 0:
            neighbors.append((new_row, new_col))

    return neighbors

#fungsi untuk mengurangi droid
def decrease_visible_droids():
    global red_droids_count, red_droids

    if len(red_droids) > 0:
        red_droids.pop()
        red_droids_count -= 1

# Daftar untuk menyimpan utas droid merah tambahan
additional_red_droid_threads = []
# Loop utama
running = True
pov_red = False
pov_green = False
randomize_map()
red_droids = []  # Inisialisasi daftar untuk droid merah
game_paused = False
red_droid_moving = False
green_droid_moving = False
stop_red_droid = False

while running:
    screen.fill(BLACK)

    draw_maze()

    if not pov_red:
        if not pov_green:
            draw_droid(GREEN, green_droid_row, green_droid_col)

    for red_droid_pos in red_droids:
        draw_droid(RED, red_droid_pos[0], red_droid_pos[1])

    draw_droid(RED, red_droid_row, red_droid_col)
    draw_menu_bar()
    pygame.display.update()  # Mengupdate layar

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if screen_width - 180 <= event.pos[0] <= screen_width - 20 and 50 <= event.pos[1] <= 550:
                    button_index = (event.pos[1] - 50) // 50
                    if button_index == 1:
                        randomize_map()
                        for i in range(len(red_droids)):
                            while True:
                                row = random.randint(0, cell_height - 1)
                                col = random.randint(0, cell_width - 1)
                                if maze[row][col] == 0 and (row, col) not in red_droids:
                                    break
                            red_droids[i] = (row, col)
                        pygame.display.flip()  # Perbarui tampilan setelah mengacak posisi droid merah
                        randomize_droid()
                    elif button_index == 0:
                        if green_droid_row == red_droid_row and green_droid_col == red_droid_col:
                            continue
                        if stop_red_droid:
                            stop_red_droid = False
                        elif not red_droid_moving:
                            red_droid_moving = True
                        # Menggerakkan droid merah utama
                        threading.Thread(target=move_red_droid).start()
                        # Menggerakkan droid merah tambahan
                        for i in range(len(red_droids)):
                            additional_red_droid_threads.append(
                                threading.Thread(target=move_additional_red_droid, args=(i,))
                            )
                            additional_red_droid_threads[-1].start()
                        
                    elif button_index == 2:
                        # Mengacak posisi droid setelah mengacak map
                        randomize_droid()
                        for i in range(len(red_droids)):
                            while True:
                                row = random.randint(0, cell_height - 1)
                                col = random.randint(0, cell_width - 1)
                                if maze[row][col] == 0 and (row, col) not in red_droids:
                                    break
                            red_droids[i] = (row, col)
                        pygame.display.flip()  # Perbarui tampilan setelah mengacak posisi droid merah
                    elif button_index == 3:
                        pov_green = not pov_green #pov droid hijau
                    elif button_index == 4:
                        change_green_droid_visibility(event.pos) #slider pov droid hijau
                    elif button_index == 5:
                        pov_red = not pov_red
                        if pov_red:
                            pov_green = False #pov droid merah
                    elif button_index == 6:
                        add_droid()  # Tambahkan droid merah baru
                    elif button_index == 7:
                        decrease_visible_droids() #mengurangi droid merah
                    elif button_index == 8:
                        stop_red_droid = True #pause game

    pygame.display.flip()

pygame.quit()