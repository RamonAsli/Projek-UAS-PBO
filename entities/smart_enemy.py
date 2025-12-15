# FILE: entities/smart_enemy.py
import pygame
import math
import random
from entities.enemy import Enemy
from settings import *

class SmartEnemy(Enemy):
    def __init__(self, x, y, image_path="enemy_smart.png"):
        super().__init__(x, y, PURPLE, image_path=image_path)

        # Resize
        target = 28
        self.frames = [pygame.transform.scale(f, (target, target)) for f in self.frames]
        self.image = self.frames[0]

        center_x = x + TILE_SIZE//2
        center_y = y + TILE_SIZE//2
        self.rect = self.image.get_rect(center=(center_x, center_y))

        self.original_frames = [f.copy() for f in self.frames]
        self.state = "PATROL"
        self.speed = ENEMY_SPEED

        self.patrol_dir = pygame.math.Vector2(0, 1)
        self.patrol_timer = 0
        
        # Variabel Warna Original untuk reset
        self.original_frames = [f.copy() for f in self.frames]

    def update(self, walls, player):
        dist_to_player = math.hypot(player.rect.centerx - self.rect.centerx, 
                                    player.rect.centery - self.rect.centery)

        if dist_to_player < DETECT_RADIUS:
            if self.state != "CHASE":
                self.state = "CHASE"
                # EFECT: Berubah Merah saat Chase (Behavior Upgrade)
                for f in self.frames:
                    f.fill((255, 50, 50), special_flags=pygame.BLEND_MULT) 
        else:
            if self.state == "CHASE":
                self.state = "PATROL"
                # Reset Warna
                self.frames = [f.copy() for f in self.original_frames]

        if self.state == "CHASE":
            self.speed = CHASE_SPEED
            self.chase(player, walls)
        else:
            self.speed = ENEMY_SPEED
            self.patrol(walls)
            
        # Animasi kedip saat chase
        if self.state == "CHASE":
            self.animate()

    def chase(self, player, walls):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        length = math.hypot(dx, dy)
        if length == 0: return
        
        dir_x = dx / length
        dir_y = dy / length

        self.rect.x += dir_x * self.speed
        self.check_collision(walls, 'x')
        self.rect.y += dir_y * self.speed
        self.check_collision(walls, 'y')

    def patrol(self, walls):
        self.rect.x += self.patrol_dir.x * self.speed
        self.check_collision(walls, 'x')
        self.rect.y += self.patrol_dir.y * self.speed
        self.check_collision(walls, 'y')

        if pygame.time.get_ticks() - self.patrol_timer > 1000:
            if random.randint(0, 50) == 0:
                self.change_dir()

    def check_collision(self, walls, axis):
        for wall in walls:
            if self.rect.colliderect(wall):
                if axis == 'x':
                    if self.rect.centerx < wall.centerx: self.rect.right = wall.left
                    else: self.rect.left = wall.right
                    if self.state == "PATROL": self.change_dir()
                elif axis == 'y':
                    if self.rect.centery < wall.centery: self.rect.bottom = wall.top
                    else: self.rect.top = wall.bottom
                    if self.state == "PATROL": self.change_dir()

    def change_dir(self):
        dirs = [pygame.math.Vector2(1,0), pygame.math.Vector2(-1,0), 
                pygame.math.Vector2(0,1), pygame.math.Vector2(0,-1)]
        self.patrol_dir = random.choice(dirs)
        self.patrol_timer = pygame.time.get_ticks()