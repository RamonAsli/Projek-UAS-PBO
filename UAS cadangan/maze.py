# FILE: maze.py
import pygame
import os
from settings import *

class Maze:
    def __init__(self, level_data, wall_texture=None, wall_color=BLUE):
        self.walls = []
        self.path_tiles = []
        self.wall_image = None
        
        # --- PENGATURAN UKURAN TEMBOK ---
        # TILE_SIZE asli = 40.
        # Kita buat tembok fisiknya lebih kecil (misal 32),
        # supaya lorong jalan terasa lebih LEBAR dan LEGA.
        self.wall_size = 32  
        # -------------------------------

        # Safety Check Warna
        if wall_color is None:
            wall_color = BLUE
        self.wall_color = wall_color
        
        # --- LOGIKA LOAD TEXTURE ---
        if wall_texture:
            path = os.path.join("assets", "images", wall_texture)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    # Resize gambar sesuai ukuran tembok yang sudah dikecilkan
                    self.wall_image = pygame.transform.scale(img, (self.wall_size, self.wall_size))
                except:
                    self.wall_image = None
        
        # Shadow color
        self.shadow_color = (max(0, self.wall_color[0]-40), 
                             max(0, self.wall_color[1]-40), 
                             max(0, self.wall_color[2]-40))
        
        self.create_walls(level_data)

    def create_walls(self, level_data):
        self.walls = []
        self.path_tiles = []
        
        # Hitung offset (geser ke tengah) supaya tembok ada di tengah-tengah kotak grid
        offset = (TILE_SIZE - self.wall_size) // 2
        
        for row_index, row in enumerate(level_data):
            for col_index, tile in enumerate(row):
                # Koordinat Grid Asli
                grid_x = col_index * TILE_SIZE
                grid_y = row_index * TILE_SIZE
                
                if tile == WALL:
                    # Buat tembok lebih kecil dan posisikan di tengah grid
                    # Ini fisik collision-nya yang mengecil
                    self.walls.append(pygame.Rect(grid_x + offset, grid_y + offset, self.wall_size, self.wall_size))
                else:
                    self.path_tiles.append((grid_x, grid_y))

    def draw(self, surface):
        for wall in self.walls:
            if self.wall_image:
                # Gambar Texture pas di kotak wall
                surface.blit(self.wall_image, wall)
            else:
                # Fallback Warna
                pygame.draw.rect(surface, self.wall_color, wall)
                # Shadow kecil
                pygame.draw.rect(surface, self.shadow_color, 
                                 (wall.x, wall.bottom - 4, wall.width, 4))
                pygame.draw.rect(surface, self.shadow_color, 
                                 (wall.right - 4, wall.y, 4, wall.height))