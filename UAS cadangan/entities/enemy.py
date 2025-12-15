import pygame
from entities.entity import Entity
from settings import *

class Enemy(Entity):
    # KITA TAMBAHKAN image_path=None DISINI
    def __init__(self, x, y, color=RED, image_path=None):
        # LALU TERUSKAN image_path KE INDUKNYA (Entity)
        super().__init__(x, y, color, "Enemy", image_path)
        self.speed = ENEMY_SPEED
    
    def update(self, walls, player):
        # Base method, to be overridden (Polymorphism)
        pass

    def apply_skin(self, image_filename):
        import os
        path = os.path.join("assets", "images", image_filename)

        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE-4, TILE_SIZE-4))
            self.frames = [img]
            self.image = img
