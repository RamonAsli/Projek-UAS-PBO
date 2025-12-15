from items.powerup import PowerUp
from settings import *

class SpeedBoost(PowerUp):
    def __init__(self, x, y):
        # Memanggil gambar "powerup_speed.png"
        super().__init__(x, y, CYAN, image_path="powerup_speed.png")
        
    def apply(self, player, game_manager):
        game_manager.active_message = "SPEED BOOST!"
        game_manager.message_timer = pygame.time.get_ticks() + 4000
        player.apply_speed_boost(3)