import pygame
import sys
import os
import json

from engine.EngineTypes import GroundType, AirType, AnimationItem # type: ignore
import engine.OBEngine as engine

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 32
SPRITE_SIZE = 16
GRID_WIDTH = 20
GRID_HEIGHT = 15
SIDEBAR_WIDTH = 200
TAB_HEIGHT = 30
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT
FPS = 60
SIDEBAR_TILE_COLS = 3
SIDEBAR_TILE_SIZE = TILE_SIZE + 4  # Extra space for padding

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_GRAY = (220, 220, 220)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OBE GUI")

# Load sprite sheet and extract tiles
def load_tiles_from_sheet(filename, tile_size) -> list[pygame.Surface]:
    sheet = pygame.image.load(filename).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    tiles = []
    for y in range(0, sheet_height, tile_size):
        for x in range(0, sheet_width, tile_size):
            tile = sheet.subsurface((x, y, tile_size, tile_size))
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))  # Scale to display size
            tiles.append(tile)
    return tiles

def createAnimClone(path, size, sequence, speed):
    return engine.AnimationPlayer(load_tiles_from_sheet(path, size), sequence=sequence, speed=speed)

tile_images: list[pygame.Surface] = load_tiles_from_sheet('./assets/images/spritesheet.png', SPRITE_SIZE)
tile_images = [createAnimClone('./assets/images/coin.png', SPRITE_SIZE, [0,1,2,3,4,5,6,7,8,9,10,11], 0.2)] + tile_images

# Create a grid
grid = [[AirType(None, pos=(x,y)) for y in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
# Tabs
tabs = ["Tiles", "Info", "Settings"]
selected_tab = "Tiles"

# Scroll settings for the sidebar
scroll_y = -10
max_scroll = max(-10, (len(tile_images) // SIDEBAR_TILE_COLS + 1) * SIDEBAR_TILE_SIZE - SCREEN_HEIGHT + 45)

# Main loop
def main():
    global scroll_y, selected_tab
    clock = pygame.time.Clock()
    running = True
    selected_tile = None
    player = None
    entities = []
    
    
    
    Animations = []

    Info_Sellected_tile = None

    while running:
        x, y = pygame.mouse.get_pos()

        grid_x = None
        grid_y = None

        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if y < TAB_HEIGHT and x > SCREEN_WIDTH - SIDEBAR_WIDTH:
                    # Click on tabs
                    tab_width = SIDEBAR_WIDTH // len(tabs)
                    tab_index = x // tab_width - 10
                    selected_tab = tabs[tab_index]
                elif x >= SCREEN_WIDTH - SIDEBAR_WIDTH:
                    
                    if selected_tab == "Tiles":
                        # Click in the sidebar for tiles
                        col = (x - (SCREEN_WIDTH - SIDEBAR_WIDTH)) // SIDEBAR_TILE_SIZE
                        row = (y - TAB_HEIGHT + scroll_y) // SIDEBAR_TILE_SIZE
                        tile_index = row * SIDEBAR_TILE_COLS + col
                        if tile_index < len(tile_images):
                            selected_tile = tile_index
                    elif selected_tab == "Info":
                        pass
                    elif selected_tab == "":
                        pass
                else:
                    # Click on the grid
                    grid_y = y // TILE_SIZE
                    grid_x = x // TILE_SIZE
                    
                    if selected_tile is not None and selected_tab == "Tiles":
                        if type(tile_images[selected_tile]) == engine.AnimationPlayer:
                            grid[grid_y][grid_x] = AnimationItem(createAnimClone('./assets/images/coin.png', SPRITE_SIZE, [0,1,2,3,4,5,6,7,8,9,10,11], 0.2), pos=(grid_x, grid_y), tile_id=selected_tile)
                        else:
                            grid[grid_y][grid_x] = GroundType(tile_images[selected_tile], pos=(grid_x, grid_y), tile_id=selected_tile)
                    elif selected_tile is not None and selected_tab == "Info":
                        Info_Sellected_tile = grid[grid_y][grid_x]


            


            elif event.type == pygame.MOUSEWHEEL:
                # Scroll in the sidebar
                if event.y > 0:
                    scroll_y = max(scroll_y - SIDEBAR_TILE_SIZE, -10)
                elif event.y < 0:
                    scroll_y = min(scroll_y + SIDEBAR_TILE_SIZE, max_scroll)
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                x, y = pygame.mouse.get_pos()
                if x < SCREEN_WIDTH - SIDEBAR_WIDTH and selected_tab == "Tiles":
                    grid_x = x // TILE_SIZE
                    grid_y = y // TILE_SIZE
                    if selected_tile is not None:
                        if type(tile_images[selected_tile]) == engine.AnimationPlayer:
                            grid[grid_y][grid_x] = AnimationItem(createAnimClone('./assets/images/coin.png', SPRITE_SIZE, [0,1,2,3,4,5,6,7,8,9,10,11], 0.2), pos=(grid_x, grid_y), tile_id=selected_tile)
                        else:
                            grid[grid_y][grid_x] = GroundType(tile_images[selected_tile], pos=(grid_x, grid_y), tile_id=selected_tile)

        

        # Draw grid
        screen.fill((135, 206, 235))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] != -1:
                    grid[y][x].draw(screen, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE)


        

        

        # Draw sidebar
        sidebar_rect = pygame.Rect(SCREEN_WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, LIGHT_GRAY, sidebar_rect)
        tab_width = SIDEBAR_WIDTH // len(tabs)
        
        
        
        
        
        
        
        if selected_tab == "Tiles":
            for i, img in enumerate(tile_images):
                col = i % SIDEBAR_TILE_COLS
                row = i // SIDEBAR_TILE_COLS
                x_pos = SCREEN_WIDTH - SIDEBAR_WIDTH + col * SIDEBAR_TILE_SIZE + 10
                y_pos = TAB_HEIGHT + row * SIDEBAR_TILE_SIZE - scroll_y
                pygame.draw.rect(screen, (0,0,0), (x_pos-2,y_pos-2, SIDEBAR_TILE_SIZE+2, SIDEBAR_TILE_SIZE+2), 1)
                if type(img) == engine.AnimationPlayer:
                    if not img.playing:
                        img.play()
                    img.update()
                    img.draw(screen, (x_pos, y_pos),(SIDEBAR_TILE_SIZE,SIDEBAR_TILE_SIZE))
                else:

                    screen.blit(img, (x_pos, y_pos))

        if selected_tab == "Info" and Info_Sellected_tile:
                InfoLines = [f"Tile Type: {Info_Sellected_tile.name}", f"Tile pos: {Info_Sellected_tile.pos}", f"Tile Id: {Info_Sellected_tile.tile_id}"]
                if type(Info_Sellected_tile) == AnimationItem:
                    AnimationEngine = Info_Sellected_tile.image
                    InfoLines.append(f"Animation Phase: {round(AnimationEngine.frame_number)}")
                    InfoLines.append(f"Total Frames: {len(AnimationEngine.frames)}")
                    InfoLines.append(f"Frame Sequence: ")
                    x = AnimationEngine.frame_order
                    formatedAnimOrder = []
                    temp = []
                    for index, item in enumerate(x):
                        if index % 8 == 0 and index != 0:
                            temp.append(item)
                            formatedAnimOrder.append(temp)
                            temp = []
                        else:
                            temp.append(item)
                    
                    for row in formatedAnimOrder:
                        InfoLines.append(f"{row}")
                    del x, temp
                    InfoLines.append(f"Frame Speed: {AnimationEngine.speed}")
                    
                    
                
                for i, line in enumerate(InfoLines):

                    
                    color = DARK_GRAY
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(line, True, BLACK)
                    screen.blit(text, (SCREEN_WIDTH - SIDEBAR_WIDTH + 20, (i * 20)+60))
                    
        for Animation in Animations:
            if not Animation.playing:
                Animation.play()
        
        
            Animation.update()
        
            Animation.draw(screen)

        for i, tab in enumerate(tabs):
            rect = pygame.Rect(SCREEN_WIDTH - SIDEBAR_WIDTH + i * tab_width, 0, tab_width, TAB_HEIGHT)
            color = DARK_GRAY if tab == selected_tab else GRAY
            pygame.draw.rect(screen, color, rect)
            font = pygame.font.SysFont(None, 24)
            text = font.render(tab, True, BLACK)
            screen.blit(text, (rect.x + 10, rect.y + 5))

        pygame.display.flip()
        clock.tick(FPS)
        
        
    # Save the grid
    
    

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
