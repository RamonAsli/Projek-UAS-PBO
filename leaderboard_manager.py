# FILE: leaderboard_manager.py
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

class LeaderboardManager:
    def __init__(self):
        self.scores = []
        self.load_scores()

    def load_scores(self):
        if os.path.exists(LEADERBOARD_FILE):
            try:
                with open(LEADERBOARD_FILE, "r") as f:
                    self.scores = json.load(f)
            except:
                self.scores = []
        else:
            self.scores = []

    def save_score(self, name, score):
        # Tambah skor baru
        self.scores.append({"name": name, "score": score})
        # Urutkan dari tertinggi ke terendah
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Ambil Top 5
        self.scores = self.scores[:5]
        
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(self.scores, f, indent=4)