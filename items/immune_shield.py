from items.powerup import PowerUp
from settings import *

class ImmuneShield(PowerUp):
    def __init__(self, x, y):
        # Memanggil gambar "powerup_shield.png"
        super().__init__(x, y, ORANGE, image_path="powerup_shield.png")
        
    def apply(self, player, game_manager):
        game_manager.active_message = "SHIELD ACTIVE!"
        game_manager.message_timer = pygame.time.get_ticks() + 2000
        player.apply_immune_shield(5)