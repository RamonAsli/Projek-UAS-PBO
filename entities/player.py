import pygame
from entities.entity import Entity
from settings import *

class Player(Entity):
    def __init__(self, x, y):
        # 1. Panggil Parent (Ini akan memuat gambar ke dalam self.frames)
        super().__init__(x, y, BLUE, "Player", image_path="player.png")
        
        # --- PERBAIKAN LOGIKA UKURAN (AGAR TETAP KECIL SAAT ANIMASI) ---
        target_size = 28
        
        # Masalah sebelumnya: Kita hanya resize self.image, tapi self.frames masih besar.
        # Solusi: Kita resize SEMUA gambar di dalam self.frames.
        new_frames = []
        for frame in self.frames:
            resized_frame = pygame.transform.scale(frame, (target_size, target_size))
            new_frames.append(resized_frame)
        
        # Timpa frames lama dengan frames yang sudah kecil
        self.frames = new_frames
        
        # Set image awal ke frame pertama yang sudah kecil
        self.image = self.frames[0]
        
        # 2. Update Rect (Hitbox) agar di Tengah Tile
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2
        self.rect = self.image.get_rect(center=(center_x, center_y))
        # -------------------------------------------------------------

        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        
        # Private variables
        self._is_immune = False
        self._immune_timer = 0
        self._speed_timer = 0
        self._immune_duration = 0
        self.original_color = BLUE

    def apply_skin(self, image_name):
        import os
    
        if not image_name:
            print("[SKIN] Tidak ada nama file skin.")
            return
        
        path = os.path.join("assets", "images", image_name)

        if not os.path.exists(path):
            print(f"[SKIN ERROR] File tidak ditemukan: {path}")
            return

        try:
            img = pygame.image.load(path).convert_alpha()

            # Resize mengikuti ukuran player saat ini
            img = pygame.transform.scale(img, (self.rect.width, self.rect.height))

            # Replace frame & image
            self.frames = [img]
            self.image = img

            # Update rect center biar tidak geser
            cx, cy = self.rect.center
            self.rect = self.image.get_rect(center=(cx, cy))

            print(f"[SKIN] Skin applied: {image_name}")

        except Exception as e:
            print(f"[SKIN ERROR] {e}")


    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        # Movement Logic
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        
        # Normalisasi vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def update(self, walls):
        self.input()
        # move() ada di parent class Entity, dia otomatis panggil animate()
        self.move(walls) 
        self.handle_powerup_timers()

    def apply_speed_boost(self, duration_sec):
        self.speed = self.base_speed * 1.5 
        self._speed_timer = pygame.time.get_ticks() + (duration_sec * 1000)
        # Visual feedback
        if not self._is_immune:
            self.image.set_alpha(150)

    def apply_immune_shield(self, duration_sec):
        self._is_immune = True
        self._immune_duration = duration_sec * 1000
        self._immune_timer = pygame.time.get_ticks() + self._immune_duration

    def handle_powerup_timers(self):
        current_time = pygame.time.get_ticks()

        # Check Speed Boost
        if self.speed != self.base_speed and current_time > self._speed_timer:
            self.speed = self.base_speed
            self.image.set_alpha(255) # Kembali normal

        # Check Immune Shield
        if self._is_immune and current_time > self._immune_timer:
            self._is_immune = False

    def is_invincible(self):
        return self._is_immune

    def draw(self, surface):
        super().draw(surface)
        if self._is_immune:
            # Gambar lingkaran pelindung
            pygame.draw.circle(surface, ORANGE, self.rect.center, 20, 2)