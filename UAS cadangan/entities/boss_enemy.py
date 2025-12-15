# FILE: entities/boss_enemy.py
import pygame
import math
from entities.smart_enemy import SmartEnemy
from settings import *

# FILE: entities/boss_enemy.py
import pygame
import math
from entities.enemy import Enemy
from settings import *
import os

class BossEnemy(Enemy):
    def __init__(self, x, y, color_override=None, image_path="boss.png"):
        # Gunakan image_path yang dikirim dari shop, fallback ke boss.png
        super().__init__(x, y, MAGENTA, image_path)

        # Resize boss agar lebih besar
        target_size = 60
        self.frames = [
            pygame.transform.scale(f, (target_size, target_size))
            for f in self.frames
        ]
        self.image = self.frames[0]

        # Posisikan di tengah tile
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2
        self.rect = self.image.get_rect(center=(center_x, center_y))

        self.speed = BOSS_SPEED
        self.name = "BOSS"

        self.zigzag_timer = 0

    def update(self, walls, player):
        # Boss selalu mengejar player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        length = math.hypot(dx, dy)

        if length == 0:
            return

        dir_x = dx / length
        dir_y = dy / length

        # Zig-zag movement
        self.zigzag_timer += 0.2
        offset = math.sin(self.zigzag_timer) * 0.6

        self.rect.x += (dir_x + offset) * self.speed
        self.check_collision(walls, 'x')

        self.rect.y += (dir_y - offset) * self.speed
        self.check_collision(walls, 'y')
