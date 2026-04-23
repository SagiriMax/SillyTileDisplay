import pygame
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

GRID_SIZE = 5 # I should've made this a json values for each tile, but I'm too lazy to rewrite it now
OUTLINE_COLOR_RED = (255, 0, 0) # this makes the json coordinates outline in red 
OUTLINE_COLOR_GREY = (150, 150, 150) # this makes the two areas outline in gray
OUTLINE_COLOR_YELLOW = (255, 255, 0) # this flashes the selected tile with yellow
OUTLINE_COLOR_ORANGE = (255, 165, 0) # <--- You can change this to "255, 255, 0" if you want to disable selected tiles flash. also check line 119 for that
BACKGROUND_COLOR = (0, 0, 0) # Change this value to change background color. uses RGB. Use (61, 192, 255) for default MMM background
OUTLINE_WIDTH = 1
MARGIN = 10  # <--- this thing barely works, I do not recommend changing it
CONFIG_FILE = "config_mmm.json" # If you need help with config files, contact @SagiriHimoto on discord or twitter
TILESET_FILE = input(f"Tileset file name (e.g. \"tstTest\"): ") + ".png" # Change this to 'tileset.png' for this script to always load tileset.png without prompt
OVERLAY_FILE_A = "overlay_a.png"  # For custom overlays. Easy
OVERLAY_FILE_B = "overlay_b.png"
OVERLAY_FILE_C = "overlay_c.png"
RENDER_SCALE = 2 # Changes the integer upscaling of the tilesets. I recommend only using 1, 2, 3 and 4. Only use positive integers.
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TILESET_FILE):
            self.callback()
def load_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config['tile_size'], config['tiles']
def load_overlay(filename):
    return pygame.image.load(filename)
def load_tileset(filename):
    return pygame.image.load(filename)
def render_tile(screen, tileset, overlay_a, overlay_b, overlay_c, tile_data, x, y, tile_size, show_overlay_a, show_overlay_b, show_overlay_c):
    coordinates = tile_data['coordinates']
    tile_rect = pygame.Rect(coordinates[0], coordinates[1], tile_size, tile_size)
    tile_image = tileset.subsurface(tile_rect)
    tile_image = pygame.transform.scale(tile_image, (tile_size * RENDER_SCALE, tile_size * RENDER_SCALE))
    screen.blit(tile_image, (x, y))
    if show_overlay_b:
        overlay_b_rect = pygame.Rect(coordinates[0], coordinates[1], tile_size, tile_size)
        overlay_b_image = overlay_b.subsurface(overlay_b_rect)
        overlay_b_image = pygame.transform.scale(overlay_b_image, (tile_size * RENDER_SCALE, tile_size * RENDER_SCALE))
        screen.blit(overlay_b_image, (x, y))
    if show_overlay_c:
        overlay_c_rect = pygame.Rect(coordinates[0], coordinates[1], tile_size, tile_size)
        overlay_c_image = overlay_c.subsurface(overlay_c_rect)
        overlay_c_image = pygame.transform.scale(overlay_c_image, (tile_size * RENDER_SCALE, tile_size * RENDER_SCALE))
        screen.blit(overlay_c_image, (x, y))
    if show_overlay_a:
        overlay_a_rect = pygame.Rect(coordinates[0], coordinates[1], tile_size, tile_size)
        overlay_a_image = overlay_a.subsurface(overlay_a_rect)
        overlay_a_image = pygame.transform.scale(overlay_a_image, (tile_size * RENDER_SCALE, tile_size * RENDER_SCALE))
        screen.blit(overlay_a_image, (x, y))
def render_grid(screen, tileset, overlay_a, overlay_b, overlay_c, selected_tile, tile_configs, offset_x, offset_y, tile_size, show_overlay_a, show_overlay_b, show_overlay_c):
    if selected_tile not in tile_configs:
        return
    config = tile_configs[selected_tile]
    display = config.get('display', [])
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            if index >= len(display):
                continue
            tile_id = display[index]
            if tile_id == 0:
                continue
            if str(tile_id) in tile_configs:
                render_tile(screen, tileset, overlay_a, overlay_b, overlay_c, tile_configs[str(tile_id)], offset_x + j * tile_size * RENDER_SCALE, offset_y + i * tile_size * RENDER_SCALE, tile_size, show_overlay_a, show_overlay_b, show_overlay_c)
def render_tileset(screen, tileset, overlay_a, overlay_b, overlay_c, tile_configs, offset_x, offset_y, tile_size, selected_tile, outline_color, show_overlay_a, show_overlay_b, show_overlay_c):
    tileset_width, tileset_height = tileset.get_size()
    scaled_tileset_width = tileset_width * RENDER_SCALE
    scaled_tileset_height = tileset_height * RENDER_SCALE
    tileset_scaled = pygame.transform.scale(tileset, (scaled_tileset_width, scaled_tileset_height))
    screen.blit(tileset_scaled, (offset_x, offset_y))
    if show_overlay_b:
        overlay_b_scaled = pygame.transform.scale(overlay_b, (scaled_tileset_width, scaled_tileset_height))
        screen.blit(overlay_b_scaled, (offset_x, offset_y))
    if show_overlay_c:
        overlay_c_scaled = pygame.transform.scale(overlay_c, (scaled_tileset_width, scaled_tileset_height))
        screen.blit(overlay_c_scaled, (offset_x, offset_y))
    if show_overlay_a:
        overlay_a_scaled = pygame.transform.scale(overlay_a, (scaled_tileset_width, scaled_tileset_height))
        screen.blit(overlay_a_scaled, (offset_x, offset_y))
    for tile_id, tile_data in tile_configs.items():
        coordinates = tile_data['coordinates']
        rect = pygame.Rect(coordinates[0] * RENDER_SCALE + offset_x, coordinates[1] * RENDER_SCALE + offset_y, tile_size * RENDER_SCALE, tile_size * RENDER_SCALE)
        pygame.draw.rect(screen, OUTLINE_COLOR_RED, rect, OUTLINE_WIDTH)
    if selected_tile in tile_configs:
        coordinates = tile_configs[selected_tile]['coordinates']
        rect = pygame.Rect(coordinates[0] * RENDER_SCALE + offset_x, coordinates[1] * RENDER_SCALE + offset_y, tile_size * RENDER_SCALE, tile_size * RENDER_SCALE)
        pygame.draw.rect(screen, outline_color, rect, OUTLINE_WIDTH)
def main():
    pygame.init()
    print("\n\n> Tile Display Program by SagiriMax")
    tile_size, tile_configs = load_config(CONFIG_FILE)
    try:
        tileset = load_tileset(TILESET_FILE)
    except Exception as e:
        print(f"Failed to load tileset: {e}")
    try:
        overlay_a = load_overlay(OVERLAY_FILE_A)
    except Exception as e:
        print(f"Failed to load overlay \"A\": {e}")
    try:
        overlay_b = load_overlay(OVERLAY_FILE_B)
    except Exception as e:
        print(f"Failed to load overlay \"B\": {e}")
    try:
        overlay_c = load_overlay(OVERLAY_FILE_C)
    except Exception as e:
        print(f"Failed to load overlay \"C\": {e}")
    tileset_width, tileset_height = tileset.get_size()
    window_width = tileset_width * RENDER_SCALE + (GRID_SIZE * tile_size * RENDER_SCALE) + 3 * MARGIN
    window_height = max(tileset_height * RENDER_SCALE, GRID_SIZE * tile_size * RENDER_SCALE) + 2 * MARGIN
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sagiri's Silly Tile Display Program")
    pygame.display.set_icon(pygame.image.load('icon.ico'))
    selected_tile = '1'
    def reload_tileset():
        nonlocal tileset
        try:
            tileset = load_tileset(TILESET_FILE)
        except Exception as e:
            print(f"Failed to reload tileset: {e}")
    # Checking for file changes, because I want it to update live
    event_handler = FileChangeHandler(reload_tileset)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(TILESET_FILE)), recursive=False)
    observer.start()
    outline_colors = [OUTLINE_COLOR_YELLOW, OUTLINE_COLOR_ORANGE]
    outline_index = 0
    outline_timer = time.time()
    overlays = {
        'F1': False,
        'F2': False,
        'F3': False,
    }
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_tile = str((int(selected_tile) - 1))
                elif event.key == pygame.K_RIGHT:
                    selected_tile = str((int(selected_tile) + 1))
                elif event.key == pygame.K_UP:
                    selected_tile = str((int(selected_tile) - 10))
                elif event.key == pygame.K_DOWN:
                    selected_tile = str((int(selected_tile) + 10))
                elif event.key == pygame.K_F1:
                    overlays['F1'] = not overlays['F1']
                elif event.key == pygame.K_F2:
                    overlays['F2'] = not overlays['F2']
                elif event.key == pygame.K_F3:
                    overlays['F3'] = not overlays['F3']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for tile_id, tile_data in tile_configs.items():
                    coordinates = tile_data['coordinates']
                    rect = pygame.Rect(coordinates[0] * RENDER_SCALE + MARGIN, coordinates[1] * RENDER_SCALE + MARGIN, tile_size * RENDER_SCALE, tile_size * RENDER_SCALE)
                    if rect.collidepoint(x, y):
                        selected_tile = str(tile_id)
                        break
        if time.time() - outline_timer > 0.07: # Change this to 0.5 or 0.8 if selected tiles flash too fast for you
            outline_index = (outline_index + 1) % len(outline_colors)
            outline_timer = time.time()
        screen.fill(BACKGROUND_COLOR)
        tileset_area_x, tileset_area_y = MARGIN, MARGIN
        grid_area_x, grid_area_y = 2 * MARGIN + tileset_width * RENDER_SCALE, MARGIN
        render_tileset(screen, tileset, overlay_a, overlay_b, overlay_c, tile_configs, tileset_area_x, tileset_area_y, tile_size, selected_tile, outline_colors[outline_index], overlays['F1'], overlays['F2'], overlays['F3'])
        render_grid(screen, tileset, overlay_a, overlay_b, overlay_c, selected_tile, tile_configs, grid_area_x, grid_area_y, tile_size, overlays['F1'], overlays['F2'], overlays['F3'])
        pygame.draw.rect(screen, OUTLINE_COLOR_GREY, (tileset_area_x - OUTLINE_WIDTH, tileset_area_y - OUTLINE_WIDTH, tileset_width * RENDER_SCALE + 2 * OUTLINE_WIDTH, tileset_height * RENDER_SCALE + 2 * OUTLINE_WIDTH), OUTLINE_WIDTH)
        pygame.draw.rect(screen, OUTLINE_COLOR_GREY, (grid_area_x - OUTLINE_WIDTH, grid_area_y - OUTLINE_WIDTH, GRID_SIZE * tile_size * RENDER_SCALE + 2 * OUTLINE_WIDTH, GRID_SIZE * tile_size * RENDER_SCALE + 2 * OUTLINE_WIDTH), OUTLINE_WIDTH)
        pygame.display.flip()
    pygame.quit()
    observer.stop()
    observer.join()
if __name__ == '__main__':
    main()
