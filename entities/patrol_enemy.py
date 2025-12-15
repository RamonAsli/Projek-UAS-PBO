import pygame
import random
from entities.enemy import Enemy
from settings import *

class PatrolEnemy(Enemy):
    def __init__(self, x, y, image_path="enemy_patrol.png"):
        super().__init__(x, y, RED, image_path=image_path)
        self.direction = pygame.math.Vector2(1, 0)
        self.move_timer = 0

    
    def update(self, walls, player):
        # Simple Logic: Move until hit wall, then random direction
        old_x, old_y = self.rect.x, self.rect.y
        self.move(walls)
        
        # If position didn't change, we hit a wall
        if self.rect.x == old_x and self.rect.y == old_y:
            self.change_direction()
            
        # Optional: Randomly change direction occasionally
        if pygame.time.get_ticks() - self.move_timer > 2000:
            self.change_direction()
            self.move_timer = pygame.time.get_ticks()

    def change_direction(self):
        directions = [pygame.math.Vector2(1, 0), pygame.math.Vector2(-1, 0),
                      pygame.math.Vector2(0, 1), pygame.math.Vector2(0, -1)]
        self.direction = random.choice(directions)