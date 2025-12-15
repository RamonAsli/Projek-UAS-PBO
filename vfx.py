# FILE: vfx.py
import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((random.randint(3, 6), random.randint(3, 6)))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Physics sederhana
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 255 # Opacity / Durasi
        self.decay = random.randint(5, 10) # Kecepatan hilang

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= self.decay
        
        if self.life <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.life)

class ParticleManager:
    def __init__(self):
        self.group = pygame.sprite.Group()

    def emit(self, x, y, color, amount=10):
        for _ in range(amount):
            p = Particle(x, y, color)
            self.group.add(p)

    def update(self):
        self.group.update()

    def draw(self, surface):
        self.group.draw(surface)