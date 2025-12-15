from items.item import Item
from settings import *

class EnergyChip(Item):
    def __init__(self, x, y):
        # Memanggil gambar "chip.png"
        super().__init__(x, y, GREEN, image_path="chip.png")
        
    def apply(self, player, game_manager):
        game_manager.add_score(1)