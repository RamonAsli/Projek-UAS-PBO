# FILE: entities/entity.py
import pygame
import os
from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, color, name="Entity", image_path=None):
        super().__init__()
        
        # --- ANIMATION SYSTEM ---
        self.frames = []
        self.frame_index = 0
        self.animation_speed = 0.1
        self.last_update = 0
        
        self.image = None
        
        # --- DEBUGGING IMAGE LOAD ---
        if image_path:
            # 1. Tentukan path lengkap
            full_path = os.path.join("assets", "images", image_path)
            
            # 2. Cek apakah file ada secara fisik
            if os.path.exists(full_path):
                try:
                    # Coba load
                    loaded = pygame.image.load(full_path).convert_alpha()
                    self.image = pygame.transform.scale(loaded, (TILE_SIZE-4, TILE_SIZE-4))
                    self.frames.append(self.image)
                    # Jika berhasil, print info sukses (Opsional, bisa dihapus nanti)
                    print(f"[SUCCESS] Loaded: {full_path}")
                except Exception as e:
                    # Jika file ada tapi error saat load (misal corrupt)
                    print(f"[ERROR] Gagal load gambar {full_path}: {e}")
            else:
                # Jika file tidak ditemukan
                # PENTING: Cek path ini di terminalmu nanti!
                print(f"[MISSING] File tidak ditemukan di: {os.path.abspath(full_path)}")
        
        # --- FALLBACK (JIKA GAMBAR GAGAL) ---
        if not self.frames:
            if image_path:
                print(f"[FALLBACK] Menggunakan kotak warna untuk {name} karena gambar gagal.")
            
            # Buat 2 frame warna (kedip dikit) untuk animasi dummy
            surf1 = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
            surf1.fill(color)
            surf2 = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
            c2 = (min(255, color[0]+30), min(255, color[1]+30), min(255, color[2]+30))
            surf2.fill(c2)
            self.frames = [surf1, surf2]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x + 2, y + 2))
        
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 0
        self.name = name

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def move(self, walls):
        self.rect.x += self.direction.x * self.speed
        self.check_collision(walls, 'x')
        self.rect.y += self.direction.y * self.speed
        self.check_collision(walls, 'y')
        
        if self.direction.magnitude() != 0:
            self.animate()

    def check_collision(self, walls, axis):
        for wall in walls:
            if self.rect.colliderect(wall):
                if axis == 'x':
                    if self.direction.x > 0: self.rect.right = wall.left
                    elif self.direction.x < 0: self.rect.left = wall.right
                elif axis == 'y':
                    if self.direction.y > 0: self.rect.bottom = wall.top
                    elif self.direction.y < 0: self.rect.top = wall.bottom

    def draw(self, surface):
        surface.blit(self.image, self.rect)