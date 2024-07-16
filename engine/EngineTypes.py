# EngineTypes.py

import pygame
import engine.OBEngine as engine

class EngineType:
    def __init__(self, name, image, pos, tile_id):
        self.name = name
        self.image = image
        self.pos = pos
        self.tile_id = tile_id

    def draw(self, screen, x, y, size):
        if self.image:
            if type(self.image) == engine.AnimationPlayer:
                if not self.image.playing:
                    self.image.play()
                self.image.update()
                self.image.draw(screen, (x, y),(size,size))
            else:
                screen.blit(self.image, (x, y, size, size))
        else:
            pygame.draw.rect(screen, (135, 206, 235), (x, y, size, size))  

class GroundType(EngineType):
    def __init__(self, image:pygame.Surface|engine.AnimationPlayer, pos:tuple=(0,0), tile_id:int=0):
        super().__init__("Ground", image, pos, tile_id)

class AirType(EngineType):
    def __init__(self, image:pygame.Surface|engine.AnimationPlayer, pos:tuple=(0,0), tile_id:int=0):
        super().__init__("Air", image, pos, tile_id)
        
class AnimationItem(EngineType):
    def __init__(self, image:pygame.Surface|engine.AnimationPlayer, pos:tuple=(0,0), tile_id:int=0):
        super().__init__("Animator", image, pos, tile_id)
    

