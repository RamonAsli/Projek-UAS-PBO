# FILE: save_manager.py
import json
import os

SAVE_FILE = "save_data.json"

class SaveManager:
    def __init__(self):
        # Default data jika file tidak ada
        self.data = {
            "coins": 0,
            "inventory": [], # List ID item yang sudah dibeli
            "equipped": {    # Item yang sedang dipakai
                "player": "default",
                "enemy": "default",
                "patrol": "default",
                "tile": "default",
                "boss": "default_boss",
                "story": None
            },
            "unlocked_levels": 1
        }
        self.load()

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    self.data = json.load(f)
            except:
                print("Save file corrupted, creating new one.")
                self.save()
        else:
            self.save()

    def save(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def reset_data(self):
        # Hapus save (Fitur request no 4)
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        self.__init__() # Re-init default data
        print("Data Reset Successful")

    def add_coins(self, amount):
        self.data["coins"] += amount
        self.save()

    def buy_item(self, item_id, price):
        if self.data["coins"] >= price and item_id not in self.data["inventory"]:
            self.data["coins"] -= price
            self.data["inventory"].append(item_id)
            self.save()
            return True
        return False

    def equip_item(self, category, item_id):
        # Pastikan item sudah dibeli atau itu default
        if item_id == "default" or item_id in self.data["inventory"]:
            self.data["equipped"][category] = item_id
            self.save()