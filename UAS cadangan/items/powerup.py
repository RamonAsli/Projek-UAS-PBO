# FILE: items/powerup.py
from items.item import Item

class PowerUp(Item):
    # Tambahkan parameter image_path=None
    def __init__(self, x, y, color, image_path=None):
        # Teruskan image_path ke induk (Item)
        super().__init__(x, y, color, image_path)
    
    def apply(self, player, game_manager):
        pass # Overridden by children