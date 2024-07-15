# EngineTypes.py

import pygame

class EngineType:
    def __init__(self, name, image, pos, tile_id):
        self.name = name
        self.image = image
        self.pos = pos
        self.tile_id = tile_id

    def draw(self, screen, x, y, size):
        # Example draw method, adjust as per your needs
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, (135, 206, 235), (x, y, size, size))  

class GroundType(EngineType):
    def __init__(self, image:pygame.Surface, pos:tuple=(0,0), tile_id:int=0):
        super().__init__("Ground", image, pos, tile_id)

class AirType(EngineType):
    def __init__(self, image:pygame.Surface, pos:tuple=(0,0), tile_id:int=0):
        super().__init__("Air", image, pos, tile_id)
