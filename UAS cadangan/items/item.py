# FILE: items/item.py
import pygame
import os
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, color, image_path=None):
        super().__init__()
        
        self.image = None
        
        # --- LOGIKA LOAD GAMBAR ---
        if image_path:
            full_path = os.path.join("assets", "images", image_path)
            if os.path.exists(full_path):
                try:
                    loaded = pygame.image.load(full_path).convert_alpha()
                    # Resize item agar pas (misal 24x24 pixel)
                    self.image = pygame.transform.scale(loaded, (36, 36))
                except:
                    pass
        
        # Fallback jika gambar tidak ada -> Pakai Kotak Warna
        if self.image is None:
            self.image = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2))
            self.image.fill(color)
            
        self.rect = self.image.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
    
    def apply(self, player, game_manager):
        pass