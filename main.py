# FILE: main.py
import pygame
import sys
import random
import os
from settings import *
from save_manager import SaveManager
from leaderboard_manager import LeaderboardManager
from vfx import ParticleManager
from maze import Maze, LEVELS
from entities.player import Player
from entities.patrol_enemy import PatrolEnemy
from entities.smart_enemy import SmartEnemy
from entities.boss_enemy import BossEnemy
from items.energy_chip import EnergyChip
from items.speed_boost import SpeedBoost
from items.immune_shield import ImmuneShield

def draw_wrapped_text(surface, text, color, x, y, font, max_width):
        words = text.split(' ')
        line = ""
        start_y = y

        for word in words:
            test_line = line + word + " "
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() > max_width:
                surface.blit(font.render(line, True, color), (x, y))
                y += font.get_height() + 5
                line = word + " "
            else:
                line = test_line

        if line:
            surface.blit(font.render(line, True, color), (x, y))
            y += font.get_height() + 5

        return y   


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Subject: Eliminated")
        self.clock = pygame.time.Clock()
        
        # Managers
        self.save_manager = SaveManager()
        self.leaderboard = LeaderboardManager()
        self.particles = ParticleManager()
        
        # Fonts
        self.font = pygame.font.SysFont("Arial", 20)
        self.book_font = pygame.font.SysFont("Courier New", 24, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 32)
        
        # Game State
        self.game_state = "MENU" 
        self.current_level_index = 0
        self.score = 0
        self.target_score = 0
        self.active_message = ""
        self.message_timer = 0
        
        self.shop_category = "player"
        self.current_book_id = None
        self.current_page = 0
        
        # Transition
        self.transition_alpha = 0
        self.transition_mode = None
        self.transition_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.transition_surface.fill(BLACK)
        
        # --- LOAD ASSETS (SOUNDS & BACKGROUND) ---
        self.sounds = {}
        self.load_sounds()
        self.background = None
        self.load_background()
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.play_bgm("bgm_menu.mp3")


    def load_background(self):
        # Coba load background.png
        bg_path = os.path.join("assets", "images", "background.png")
        if os.path.exists(bg_path):
            try:
                img = pygame.image.load(bg_path).convert()
                # Resize agar pas layar
                self.background = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                print("Error loading background image.")
                self.background = None
        else:
            self.background = None # Jika tidak ada, nanti pakai fill BLACK

    def load_sounds(self):
        def load_snd(name, filename):
            path = os.path.join("assets", "sounds", filename)
            if os.path.exists(path): self.sounds[name] = pygame.mixer.Sound(path)
            else: self.sounds[name] = None
        load_snd('collect', 'coin.wav')
        load_snd('powerup', 'powerup.wav')
        load_snd('win', 'win.wav')
        load_snd('lose', 'lose.wav')

    def play_sound(self, name):
        if self.sounds.get(name): self.sounds[name].play()
    
    def play_bgm(self, filename, volume=0.4, loop=-1):
        pygame.mixer.music.stop()
        path = os.path.join("assets", "sounds", filename)
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop)


    def get_color_from_id(self, item_id, default_color):
        if item_id == "default": return default_color
        for item in SHOP_ITEMS:
            if item['id'] == item_id: return item['color']
        return default_color

    def start_transition(self, mode, callback=None):
        self.transition_mode = mode
        self.transition_alpha = 0 if mode == "OUT" else 255
        self.transition_callback = callback
    
    def get_texture_from_id(self, item_id, default_val=None):
        if item_id == "default": return default_val
        for item in SHOP_ITEMS:
            if item['id'] == item_id:
                return item.get('image', default_val)
        return default_val

    def setup_level(self, level_index):
        self.all_sprites.empty()
        self.enemies.empty()
        self.items.empty()
        self.score = 0
        
        level_data = LEVELS[level_index]
        
        tile_skin_id = self.save_manager.data['equipped']['tile']
        tile_color = self.get_color_from_id(tile_skin_id, BLUE)
        tile_texture = self.get_texture_from_id(tile_skin_id, "wall_default.png")
        self.maze = Maze(level_data, wall_texture=tile_texture ,wall_color=tile_color)
        
        player_skin_id = self.save_manager.data['equipped']['player']
        skin_file = self.get_texture_from_id(player_skin_id)

        player_spawned = False

        for r, row in enumerate(level_data):
            for c, tile in enumerate(row):
                if tile == PLAYER_START:
                    self.player = Player(c*TILE_SIZE, r*TILE_SIZE)
                    self.all_sprites.add(self.player)
                    player_spawned = True

                    # APPLY SKIN SETELAH PLAYER ADA
                    if skin_file:
                        self.player.apply_skin(skin_file)

                    shield_x = (c + 1) * TILE_SIZE
                    shield_y = r * TILE_SIZE
                    start_shield = ImmuneShield(shield_x, shield_y)
                    self.all_sprites.add(start_shield)
                    self.items.add(start_shield)
        
        if not player_spawned:
            self.player = Player(40, 40)
            self.all_sprites.add(self.player)

        is_boss_level = (level_index == 9)
        num_chips = 3 + level_index
        num_enemies = 2 + int(level_index * 1.5)
        num_powerups = 3
        
        self.target_score = num_chips 
        if not self.maze.path_tiles: return

        self.spawn_random_object(EnergyChip, num_chips)
        
        if is_boss_level:
            boss_skin_id = self.save_manager.data['equipped']['boss']
            boss_skin_file = self.get_texture_from_id(boss_skin_id, "boss.png")

            self.spawn_boss_enemy(BossEnemy, boss_skin_file)

            self.spawn_random_enemies(SmartEnemy, 2, PURPLE)
        else:
            smart_skin = self.save_manager.data['equipped']['enemy']
            patrol_skin = self.save_manager.data['equipped']['patrol']
            
            
            smart_count = level_index // 3
            patrol_count = num_enemies - smart_count
            self.spawn_random_enemies(PatrolEnemy, patrol_count, patrol_skin)
            self.spawn_random_enemies(SmartEnemy, smart_count, smart_skin)
        
        self.spawn_random_object(SpeedBoost, num_powerups // 2)
        self.spawn_random_object(ImmuneShield, num_powerups - (num_powerups // 2))

    def spawn_boss_enemy(self, obj_class, image_file):
        if not self.maze.path_tiles:
            return
        spawn_pos = random.choice(self.maze.path_tiles)
        boss = obj_class(spawn_pos[0], spawn_pos[1], image_path=image_file)
        self.all_sprites.add(boss)
        self.enemies.add(boss)

    def spawn_random_object(self, obj_class, count):
        for _ in range(count):
            if not self.maze.path_tiles: break
            spawn_pos = random.choice(self.maze.path_tiles)
            new_obj = obj_class(spawn_pos[0], spawn_pos[1])
            self.all_sprites.add(new_obj)
            self.items.add(new_obj)

    def spawn_random_enemies(self, obj_class, count, skin_id):
        for _ in range(count):
            if not self.maze.path_tiles:
                break

            spawn_pos = random.choice(self.maze.path_tiles)

            # DUIT ITEM ↓
            skin_file = self.get_texture_from_id(skin_id, None)

            enemy = obj_class(spawn_pos[0], spawn_pos[1], image_path=skin_file)

            self.enemies.add(enemy)
            self.all_sprites.add(enemy)


    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if self.transition_mode: continue 

            if event.type == pygame.KEYDOWN:
                if self.game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        self.start_transition("OUT", lambda: self.start_game(0))
                    elif event.key == pygame.K_l: self.game_state = "LEVEL_SELECT"
                    elif event.key == pygame.K_s: self.game_state = "SHOP"
                    elif event.key == pygame.K_h: self.game_state = "HOWTO"
                    elif event.key == pygame.K_b: self.game_state = "LEADERBOARD"
                    elif event.key == pygame.K_c: self.game_state = "LIBRARY"
                    elif event.key == pygame.K_q: pygame.quit(); sys.exit()
                    elif event.key == pygame.K_DELETE:
                        self.save_manager.reset_data()
                        self.active_message = "DATA RESET!"
                        self.message_timer = pygame.time.get_ticks() + 2000

                elif self.game_state == "LEADERBOARD":
                    if event.key == pygame.K_ESCAPE: self.game_state = "MENU"

                elif self.game_state == "LEVEL_SELECT":
                    if event.key == pygame.K_ESCAPE: self.game_state = "MENU"
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        self.start_transition("OUT", lambda: self.start_game(idx))
                    elif event.key == pygame.K_0:
                        self.start_transition("OUT", lambda: self.start_game(9))
                
                elif self.game_state == "HOWTO":
                    if event.key == pygame.K_ESCAPE: self.game_state = "MENU"
                        


                elif self.game_state == "SHOP":
                    if event.key == pygame.K_ESCAPE: self.game_state = "MENU"

                elif self.game_state == "LIBRARY":
                    if event.key == pygame.K_ESCAPE: self.game_state = "MENU"

                elif self.game_state == "READER":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "LIBRARY"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                        story_pages = STORY_DATA.get(self.current_book_id, [])
                        if self.current_page < len(story_pages) - 1:
                            self.current_page += 1
                            self.play_sound('powerup')
                    elif event.key == pygame.K_LEFT:
                        if self.current_page > 0:
                            self.current_page -= 1
                            self.play_sound('powerup')

                elif self.game_state == "PLAYING":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.game_state = "PAUSED"

                elif self.game_state == "PAUSED":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.game_state = "PLAYING"
                    elif event.key == pygame.K_m: self.game_state = "MENU"
                    elif event.key == pygame.K_q: pygame.quit(); sys.exit()

                elif self.game_state in ["WIN", "LOSE", "LEVEL_UP"]:
                    if event.key == pygame.K_r: self.start_game(self.current_level_index)
                    elif event.key == pygame.K_m: self.game_state = "MENU"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "SHOP": self.handle_shop_click(event.pos)
                elif self.game_state == "LIBRARY": self.handle_library_click(event.pos)

    def start_game(self, level_idx):
        self.current_level_index = level_idx
        self.setup_level(level_idx)
        self.game_state = "PLAYING"
        self.transition_mode = "IN"
        self.play_bgm("bgm_game.mp3")

    def handle_shop_click(self, pos):
        mx, my = pos
        # Tab Logic
        if my < 120:
            tab_list = ["player", "enemy", "patrol", "boss", "tile", "story"]
            x = 50   
            width = 200
            for tab in tab_list:
                if x < mx < x + width:
                    self.shop_category = tab
                    return
                x += 210  # jarak antar tab

        
        start_y = 150
        filtered_items = [i for i in SHOP_ITEMS if i['cat'] == self.shop_category]
        for i, item in enumerate(filtered_items):
            item_y = start_y + (i * 60)
            if 100 < mx < 1000 and item_y < my < item_y + 50:
                
                # --- LOGIKA KLIK BARU ---
                is_default = (item['id'] == "default")
                is_in_inventory = (item['id'] in self.save_manager.data['inventory'])
                
                # Jika item "Default" ATAU sudah dibeli -> Langsung Equip
                if is_default or is_in_inventory:
                    if item['cat'] != 'story':
                        self.save_manager.equip_item(item['cat'], item['id'])
                        self.play_sound('powerup')
                else:
                    # Jika belum punya -> Beli dulu
                    if self.save_manager.buy_item(item['id'], item['price']):
                        self.play_sound('collect')
                    else:
                        self.play_sound('lose')

    def handle_library_click(self, pos):
        mx, my = pos
        has_book = "sty_journal" in self.save_manager.data['inventory']
        button_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 50, 400, 100)
        
        if has_book and button_rect.collidepoint((mx, my)):
            self.current_book_id = "sty_journal"
            self.current_page = 0
            self.game_state = "READER"
            self.play_sound('collect')

    def update(self):
        self.particles.update()

        if self.transition_mode == "OUT":
            self.transition_alpha += 10
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.transition_mode = "IN"
                if self.transition_callback: self.transition_callback()
        elif self.transition_mode == "IN":
            self.transition_alpha -= 10 
            if self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transition_mode = None

        if self.game_state == "PLAYING" and not self.transition_mode:
            self.player.update(self.maze.walls)
            
            for enemy in self.enemies:
                enemy.update(self.maze.walls, self.player)

            hit_list = pygame.sprite.spritecollide(self.player, self.items, True)
            for item in hit_list:
                item.apply(self.player, self)
                color = GREEN
                if isinstance(item, SpeedBoost): color = CYAN
                elif isinstance(item, ImmuneShield): color = ORANGE
                self.particles.emit(item.rect.centerx, item.rect.centery, color)
                
                if isinstance(item, EnergyChip):
                    self.play_sound('collect')
                    self.save_manager.add_coins(10)
                else:
                    self.play_sound('powerup')
            
            if not self.player.is_invincible():
                if pygame.sprite.spritecollide(self.player, self.enemies, False):
                    self.game_state = "LOSE"
                    self.play_sound('lose')
                    self.leaderboard.save_score("Player", self.score * 10)

            if pygame.time.get_ticks() > self.message_timer:
                self.active_message = ""

    def add_score(self, amount):
        self.score += amount
        if self.score >= self.target_score:
            if self.current_level_index < len(LEVELS) - 1:
                self.play_sound('win')
                next_level = self.current_level_index + 1
                self.start_transition("OUT", lambda: self.start_game(next_level))
            else:
                self.game_state = "WIN"
                self.play_sound('win')
                self.leaderboard.save_score("Player", self.score * 100)

    def draw(self):
        # --- DRAW BACKGROUND ---
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK) # Fallback kalau gambar ga ada
        
        # --- DRAW STATES ---
        if self.game_state == "MENU": self.draw_menu()
        elif self.game_state == "LEVEL_SELECT": self.draw_level_select()
        elif self.game_state == "SHOP": self.draw_shop()
        elif self.game_state == "LEADERBOARD": self.draw_leaderboard()
        elif self.game_state == "HOWTO": self.draw_howto()
        elif self.game_state == "LIBRARY": self.draw_library()
        elif self.game_state == "READER": self.draw_reader()
        
        elif self.game_state == "PLAYING" or self.game_state == "PAUSED":


            self.maze.draw(self.screen)
            self.particles.draw(self.screen)
            self.all_sprites.draw(self.screen)
            
            if self.player.is_invincible():
                pygame.draw.rect(self.screen, ORANGE, self.player.rect, 2)
            
            self.draw_hud()
            
            if self.active_message:
                msg_text = self.font.render(self.active_message, True, YELLOW)
                self.screen.blit(msg_text, (SCREEN_WIDTH//2 - msg_text.get_width()//2, 80))
            
            if self.game_state == "PAUSED": self.draw_pause_menu()
                
        elif self.game_state in ["WIN", "LOSE", "LEVEL_UP"]:
            self.draw_centered_text(self.game_state, WHITE, 0, self.title_font)
            self.draw_centered_text("Press M for Menu", GRAY, 50)

        if self.transition_alpha > 0:
            self.transition_surface.set_alpha(self.transition_alpha)
            self.screen.blit(self.transition_surface, (0,0))

        pygame.display.flip()

    def draw_hud(self):
        hud_y = 0
        hud_bg = pygame.Surface((SCREEN_WIDTH, 30))
        hud_bg.set_alpha(200)
        hud_bg.fill((20, 20, 30))
        self.screen.blit(hud_bg, (0, hud_y))
        
        pygame.draw.line(self.screen, GRAY, (0, hud_y), (SCREEN_WIDTH, hud_y), 2)
        
        info_left = f"LVL: {self.current_level_index + 1} | CHIPS: {self.score}/{self.target_score}"
        txt_left = self.font.render(info_left, True, WHITE)
        self.screen.blit(txt_left, (20, hud_y + 15))
        
        info_coin = f"COINS: {self.save_manager.data['coins']}"
        txt_coin = self.font.render(info_coin, True, GOLD) 
        self.screen.blit(txt_coin, (SCREEN_WIDTH - 350, hud_y + 15))

        x_offset = SCREEN_WIDTH - 150
        current_time = pygame.time.get_ticks()
        
        if self.player.is_invincible():
            time_left = max(0, (self.player._immune_timer - current_time) // 100)
            pygame.draw.circle(self.screen, ORANGE, (x_offset, hud_y + 25), 15)
            t_txt = self.font.render(str(time_left), True, WHITE)
            self.screen.blit(t_txt, (x_offset-5, hud_y + 15))
            x_offset += 50

        if self.player.speed > PLAYER_SPEED:
            time_left = max(0, (self.player._speed_timer - current_time) // 100)
            pygame.draw.circle(self.screen, CYAN, (x_offset, hud_y + 25), 15)
            t_txt = self.font.render(str(time_left), True, WHITE)
            self.screen.blit(t_txt, (x_offset-5, hud_y + 15))

    def draw_shop(self):
        self.draw_centered_text("ITEM SHOP", GOLD, -320, font=self.title_font)
        
        tabs = ["player", "S enemy", "D enemy", "boss", "tile", "story"]
        start_x = 50
        for tab in tabs:
            color = WHITE if self.shop_category == tab else GRAY
            pygame.draw.rect(self.screen, color, (start_x, 80, 200, 40))
            txt = self.font.render(tab.upper(), True, BLACK)
            self.screen.blit(txt, (start_x + 60, 90))
            start_x += 210

        start_y = 150
        filtered = [i for i in SHOP_ITEMS if i['cat'] == self.shop_category]
        for i, item in enumerate(filtered):
            y = start_y + (i * 60)
            s = pygame.Surface((900, 50))
            s.set_alpha(150)
            s.fill((30, 30, 30))
            self.screen.blit(s, (100, y))
            
            # Icon
            if "image" in item:
                icon_path = os.path.join("assets", "images", item["image"])
                if os.path.exists(icon_path):
                    icon = pygame.image.load(icon_path).convert_alpha()
                    icon = pygame.transform.scale(icon, (40, 40))
                    self.screen.blit(icon, (110, y+5))
                else:
                    pygame.draw.rect(self.screen, item['color'], (110, y+5, 40, 40))

            
            name = self.font.render(item['name'], True, WHITE)
            self.screen.blit(name, (170, y+15))
            
            # --- LOGIKA TOMBOL BARU ---
            # Cek: Default Item SELALU dimiliki
            is_default = (item['id'] == "default")
            is_in_inventory = (item['id'] in self.save_manager.data['inventory'])
            
            owned = is_default or is_in_inventory
            
            equipped = self.save_manager.data['equipped'].get(item['cat']) == item['id']
            
            btn_color = GREEN if equipped else (CYAN if owned else YELLOW)
            
            if item['cat'] == 'story':
                btn_txt = "OWNED" if owned else f"BUY {item['price']}"
                if owned: btn_color = GRAY
            else:
                btn_txt = "EQUIPPED" if equipped else ("EQUIP" if owned else f"BUY {item['price']}")

            pygame.draw.rect(self.screen, btn_color, (800, y+10, 150, 30))
            b_surf = self.font.render(btn_txt, True, BLACK)
            self.screen.blit(b_surf, (810, y+15))
        
        self.draw_centered_text("Press [ESC] Back", GRAY, 350)

    def draw_library(self):
        self.draw_centered_text("SECRET ARCHIVES", GOLD, -250, font=self.title_font)
        
        has_book = "sty_journal" in self.save_manager.data['inventory']
        rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 50, 400, 100)
        
        if has_book:
            pygame.draw.rect(self.screen, CYAN, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 4)
            pygame.draw.rect(self.screen, WHITE, (rect.x + 20, rect.y + 20, 50, 60))
            pygame.draw.line(self.screen, BLACK, (rect.x + 45, rect.y + 20), (rect.x + 45, rect.y + 80), 2)
            text = self.info_font.render("READ JOURNAL", True, BLACK)
            self.screen.blit(text, (rect.x + 90, rect.y + 35))
            self.draw_centered_text("Click to Open", GRAY, 80)
        else:
            pygame.draw.rect(self.screen, (50, 50, 50), rect)
            pygame.draw.rect(self.screen, RED, rect, 2)
            text = self.info_font.render("LOCKED", True, RED)
            self.screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - 15))
            self.draw_centered_text("Buy 'The Lost Journal' in Shop", GRAY, 80)

        self.draw_centered_text("Press [ESC] Back", RED, 300)

    
    


    def draw_reader(self):
        bg_rect = pygame.Rect(100, 50, SCREEN_WIDTH-200, SCREEN_HEIGHT-100)
        pygame.draw.rect(self.screen, (20, 20, 30), bg_rect)
        pygame.draw.rect(self.screen, CYAN, bg_rect, 4)
        
        pages = STORY_DATA.get(self.current_book_id, ["DATA CORRUPTED"])
        content = pages[self.current_page]
        
        lines = content.split('\n')
                # --- DRAW PARAGRAPHS WITH WRAPPING ---
        paragraphs = content.split("\n\n")   # Pisah paragraf

        y_text = 150
        max_width = SCREEN_WIDTH - 350

        for para in paragraphs:
            y_text = draw_wrapped_text(
                self.screen,
                para,
                GREEN,
                150,
                y_text,
                self.book_font,
                max_width
            )
            y_text += 25   # jarak antar paragraf


            
        page_info = f"PAGE {self.current_page + 1} / {len(pages)}"
        pg_surf = self.font.render(page_info, True, WHITE)
        self.screen.blit(pg_surf, (SCREEN_WIDTH//2 - pg_surf.get_width()//2, SCREEN_HEIGHT - 100))
        
        nav_hint = "[LEFT] PREV   |   [RIGHT/SPACE] NEXT   |   [ESC] CLOSE"
        nav_surf = self.font.render(nav_hint, True, GRAY)
        self.screen.blit(nav_surf, (SCREEN_WIDTH//2 - nav_surf.get_width()//2, SCREEN_HEIGHT - 40))

    def draw_leaderboard(self):
        self.draw_centered_text("TOP SCORERS", GOLD, -200, font=self.title_font)
        y = 200
        for idx, entry in enumerate(self.leaderboard.scores):
            txt = f"{idx+1}. {entry['name']} - {entry['score']}"
            surf = self.info_font.render(txt, True, WHITE)
            self.screen.blit(surf, (SCREEN_WIDTH//2 - 100, y))
            y += 50
        self.draw_centered_text("Press [ESC] Back", RED, 250)

    def draw_menu(self):
        self.draw_centered_text("Subject: Eliminated", PURPLE, -180, font=self.title_font)
        opts = ["[SPACE] PLAY", "[L] LEVEL SELECT", "[S] SHOP", "[B] LEADERBOARD", "[C] COLLECTION","[H] HELP","[Q] QUIT"]
        for i, opt in enumerate(opts):
            self.draw_centered_text(opt, WHITE, -50 + (i*50))
        self.draw_centered_text("[DEL] RESET DATA", RED, 280)
        
        coin_text = f"TOTAL COINS: {self.save_manager.data['coins']}"
        coin_surf = self.info_font.render(coin_text, True, GOLD) 
        self.screen.blit(coin_surf, (30, SCREEN_HEIGHT - 60))

    def draw_level_select(self):
        # Judul
        self.draw_centered_text("SELECT LEVEL", CYAN, -250, font=self.title_font)
        self.draw_centered_text("Press Keyboard Number (1-9, 0 = Level 10)", GRAY, -180)
        
        # --- PENGATURAN GRID YANG RAPI ---
        box_width = 120
        box_height = 80
        gap_x = 60  # Jarak antar kotak horizontal
        gap_y = 50  # Jarak antar kotak vertikal
        cols = 5    # Jumlah kolom per baris
        
        # Hitung lebar total grid agar bisa ditaruh pas di tengah layar
        total_grid_width = (cols * box_width) + ((cols - 1) * gap_x)
        start_x = (SCREEN_WIDTH - total_grid_width) // 2
        start_y = 250
        
        for i in range(10):
            row = i // cols
            col = i % cols
            
            x = start_x + (col * (box_width + gap_x))
            y = start_y + (row * (box_height + gap_y))
            
            rect = pygame.Rect(x, y, box_width, box_height)
            
            # Gambar Kotak (Desain Sci-Fi)
            # 1. Background kotak (Gelap transparan dikit kalau mau, disini solid gelap)
            pygame.draw.rect(self.screen, (20, 30, 40), rect) 
            # 2. Border Neon
            pygame.draw.rect(self.screen, CYAN, rect, 2)
            
            # Teks Angka (Di tengah kotak)
            level_num = str(i + 1)
            num_surf = self.title_font.render(level_num, True, WHITE)
            num_rect = num_surf.get_rect(center=rect.center) # Center text inside rect
            self.screen.blit(num_surf, num_rect)
            
        self.draw_centered_text("Press [ESC] Back", RED, 300)

    def draw_howto(self):
        self.draw_centered_text("HELP SCREEN", BLUE, -200, font=self.title_font)
        instructions = [
            "1. Move with W, A, S, D",
            "2. Collect Chips & Powerups for easy gameplay",
            "3. Avoid Enemies or you die",
            "4. Press ESC to Pause the Games",
            "5. Buy Skins in Shop"
        ]
        for i, line in enumerate(instructions):
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i * 40))
        self.draw_centered_text("Press [ESC] Back", RED, 250)

    def draw_pause_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        self.draw_centered_text("PAUSED", CYAN, -100, font=self.title_font)
        self.draw_centered_text("Press [ESC] to Resume", WHITE, 0)
        self.draw_centered_text("Press [M] Return to Menu", YELLOW, 50)
        self.draw_centered_text("Press [Q] Quit Game", RED, 100)

    def draw_centered_text(self, text, color, y_offset, font=None):
        if font is None: font = self.info_font
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
        self.screen.blit(surface, rect)

if __name__ == "__main__":
    game = GameManager()
    game.run()