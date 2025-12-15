# FILE: settings.py
import pygame

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 40
FPS = 60

# Colors (Basic)
WHITE = (255, 255, 255)
BLACK = (10, 10, 15)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (255, 215, 0)
CYAN = (0, 255, 255)
PURPLE = (150, 0, 150)
ORANGE = (255, 165, 0)
GOLD = (218, 165, 32) 
MAGENTA = (255, 0, 255)

# --- SHOP DATA (DATABASE BARANG) ---

SHOP_ITEMS = [
    # --- DEFAULT SKINS (ID UNIK) ---
    {"id": "default_player", "cat": "player", "name": "Default Suit", "price": 0, "color": BLUE, "image": "player.png"},
    {"id": "default_smart", "cat": "enemy", "name": "Default Smart", "price": 0, "color": PURPLE, "image": "enemy_smart.png"},
    {"id": "default_patrol", "cat": "patrol", "name": "Default Patrol", "price": 0, "color": RED, "image": "enemy_patrol.png"},
    {"id": "default_tile", "cat": "tile", "name": "Standard Lab", "price": 0, "color": (100, 100, 200), "image": "wall_default.png"},

    # Player skins
    {"id": "p_neon", "cat": "player", "name": "Neon Armor", "price": 50, "color": CYAN, "image": "player_neon.png"},

    # Smart enemy skins
    {"id": "e_dark", "cat": "enemy", "name": "Dark Hunter", "price": 50, "color": BLUE, "image": "enemy_dark.png"},

    # Patrol skins
    {"id": "pt_police", "cat": "patrol", "name": "Police Bot", "price": 50, "color": BLUE, "image": "enemy_police.png"},

    #Boss Skins
    {"id": "default_boss", "cat": "boss", "name": "Default Boss", "price": 0, "color":MAGENTA, "image": "boss.png"},
    {"id": "boss_dark", "cat": "boss", "name": "Dark Overlord", "price": 100, "color":MAGENTA,"image": "boss_dark.png"},

    # Tile themes
    {"id": "t_forest", "cat": "tile", "name": "Forest Lab", "price": 50, "color": (34, 139, 34), "image": "wall_forest.png"},

    # Story
    {"id": "sty_journal", "cat": "story", "name": "The Lost Journal", "price": 200, "color": WHITE},
]


# --- ISI CERITA (SATU BUKU BANYAK HALAMAN) ---
# Kuncinya: "id_item": [List Halaman 1, Halaman 2, dst...]
STORY_DATA = {
    "sty_journal": [
    "PAGE 1/10 - ORIGIN\n\nTahun 2144, Nexus Laboratory memulai proyek terbesar yang pernah dikerjakan umat manusia: Quantum Source Initiative.\n\nTujuan proyek ini sederhana namun mustahil—menciptakan sumber energi tak terbatas dengan memanfaatkan retakan dimensi mikro.\n\nTidak ada yang tahu bahwa retakan itu bukan sekadar fenomena fisika… tetapi pintu menuju sesuatu yang jauh lebih tua dari konsep ruang dan waktu.",
    
    "PAGE 2/10 - FIRST CONTACT\n\nRetakan pertama terbentuk pada 14 Mei 2145. Cahaya hijau gelap memancar dari ruang uji dan bentuk samar muncul di balik kabut dimensi.\n\nDr. Voss: \"…Kau lihat itu? Ada sesuatu di balik retakan.\"\nDr. Albedo: \"Itu bukan energi biasa. Itu… sedang mengamati kita.\"\n\nSejak hari itu, laboratorium mulai mengalami fenomena yang tak dapat dijelaskan: suara langkah, bayangan yang mengikuti peneliti, dan mesin aktif tanpa disentuh.",
    
    "PAGE 3/10 - THE ENTITIES\n\nEktoplasma yang kami ekstraksi dari retakan menunjukkan pola perilaku seperti organisme.\n\nBeberapa mencoba meniru suara manusia. Beberapa mengikuti sumber panas. Beberapa bergerak dalam kelompok kecil.\n\nKami menamai mereka \"Subjects\".\nSubject 01–05 menunjukkan kecerdasan dasar—mereka belajar dari pola pergerakan penjaga dan mencoba membuka pintu laboratorium.\n\nNamun satu entitas berbeda.",
    
    "PAGE 4/10 - SUBJECT 99\n\nDi tengah kekacauan eksperimen awal, kami menciptakan prototipe terakhir: Subject 99.\n\nTidak seperti entitas lain yang agresif, 99 hanya menyerap energi dan partikel sisa dari eksperimen gagal.\n\nBentuknya sederhana, geometris, dan stabil. Ia mengikuti perintah, tidak menyerang, dan… lapar secara konstan.\n\nDr. Albedo: \"Akhirnya… satu entitas yang tidak mencoba membunuh kita. Kita menyebutnya: Cleaner Unit. Atau… Muncher.\"",
    
    "PAGE 5/10 - THE WARNING\n\nPada hari ke-129 eksperimen, retakan mulai berdenyut seperti organ hidup.\n\n\"Jangan mendekatkan instrumen ke celah itu!\" — Dr. Voss\n\nAlat ukur menangkap sesuatu mirip detak jantung, dan setiap denyut memperluas retakan beberapa milimeter.\n\nKami mulai menyadari sesuatu: entitas-entitas itu tidak sekadar tercipta—mereka masuk dari suatu tempat lain.",
    
    "PAGE 6/10 - BREACH EVENT\n\n7 November 2145, pukul 02:14 — alarm berbunyi.\n\nSubject 01–05 membobol sistem keamanan, menonaktifkan pintu isolasi, dan mengunci seluruh divisi bawah tanah. Mereka telah belajar dari kebiasaan kami.\n\nRekaman CCTV terakhir menunjukkan Subject 03 membuka panel listrik dan memutuskan aliran utama.\n\nTidak ada yang dapat keluar. Termasuk aku.",
    
    "PAGE 7/10 - THE LAST PROTOCOL\n\nDalam kondisi terisolasi, kami mengaktifkan Protokol Akhir: membakar seluruh dokumen, menghapus database, dan mengevakuasi semua personel ke permukaan.\n\nNamun hanya sedikit yang berhasil keluar sebelum ventilasi dibanjiri energi ektoplasma.\n\nAku memilih bertahan di sini untuk menyelesaikan satu hal terakhir.\n\nJika ada yang membaca ini, berarti kamu menemukan jurnal ini lebih dulu daripada mereka.",
    
    "PAGE 8/10 - FINAL NOTE FROM DR. ALBEDO\n\nAku meninggalkan catatan ini untuk siapa pun yang mampu melanjutkan pekerjaanku.\n\nSubject 99 berbeda dari entitas lain. Ia tidak agresif, tidak terhubung ke retakan, dan tidak memiliki keinginan membunuh.\n\nIa satu-satunya yang dapat menyerap energi residu dari retakan tanpa menjadi korup atau bermutasi.\n\nJika dunia masih memiliki harapan… itu berada pada makhluk kecil itu.",
    
    "PAGE 9/10 - INSTRUCTIONS\n\nUntuk menghentikan ekspansi retakan, 99 harus mengumpulkan semua Energy Chips di setiap sektor laboratorium.\n\nChips itu merupakan fragmen stabilisasi yang kami ciptakan, dan jika semuanya dikembalikan ke mesin inti, portal akan menutup dengan sendirinya.\n\nNamun ingat—Subjects lain tidak akan diam. Mereka punya tujuan berbeda.\nMereka ingin portal itu tetap terbuka.",
    
    "PAGE 10/10 - MY FINAL MOMENT\n\nAku bisa mendengar mereka di balik pintu… langkah cepat, gesekan dinding, dan suara lirih menyerupai bisikan manusia.\n\nWaktuku tinggal sedikit.\n\nJika kamu menemukan Subject 99… bimbing dia. Jangan biarkan dia menyerap energi sembarangan. Jangan biarkan ia jatuh ke tangan entitas lain.\n\nTutup retakan itu.\nSelamatkan dunia ini.\n\n- Dr. Albedo, Peneliti Utama Nexus Laboratory"
]



}


# Gameplay
PLAYER_SPEED = 5
ENEMY_SPEED = 2
CHASE_SPEED = 3.5
DETECT_RADIUS = 100
BOSS_SPEED = 4       # Speed Boss
BOSS_DETECT_RADIUS = 500 # Boss deteksi jauh

# Map Tags
WALL = '1'
PLAYER_START = 'P'

# --- 10 NEW FULLY CONNECTED LEVELS ---
# Ukuran Grid: 32 Kolom x 18 Baris
# Pastikan semua '0' terhubung ke 'P'

# LEVEL 1: The Training Hall (Ruangan luas, banyak pilar)
LEVEL_1 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10110110110110110110110110110101",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "11111111111111111111111111111111",
]

# LEVEL 2: The Loop (Dua jalur utama melingkar dengan penghubung)
LEVEL_2 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "10111111111111100111111111111101",
    "10100000000000100100000000000101",
    "10101111111110100101111111110101",
    "10101000000010100101000000010101",
    "10101011111010100101011111010101",
    "10101010000010100101000001010101",
    "10000000011110000001111000000001", # Konektor Tengah
    "10000000011110000001111000000001",
    "10101010000010100101000001010101",
    "10101011111010100101011111010101",
    "10101000000010100101000000010101",
    "10101111111110100101111111110101",
    "10100000000000100100000000000101",
    "10111111111111100111111111111101",
    "10000000000000000000000000000001",
    "11111111111111111111111111111111",
]

# LEVEL 3: Four Rooms (4 Ruangan besar yang saling terhubung)
LEVEL_3 = [
    "11111111111111111111111111111111",
    "1P000000011111100111111000000001",
    "10111111010000100100001011111101",
    "10100000010000100100001000000101",
    "10100000010000100100001000000101",
    "10111111010000100100001011111101",
    "10000000000000000000000000000001", # Main Hallway
    "10111111011111100111111011111101",
    "10100000010000000000001000000101",
    "10100001010000000000001010000101",
    "10111111011111100111111011111101",
    "10000000000000000000000000000001", # Main Hallway
    "10111111010000100100001011111101",
    "10100000010000100100001000000101",
    "10100000010000100100001000000101",
    "10111111010000100100001011111101",
    "10000000011111100111111000000001",
    "11111111111111111111111111111111",
]

# LEVEL 4: The City Block (Banyak simpangan kecil seperti kota)
LEVEL_4 = [
    "11111111111111111111111111111111",
    "10000100010001000100010001000001",
    "10110101010101010101010101011101",
    "10100001000100010001000100000101",
    "10101111111111111111111111110101",
    "10100001000100010001000100000101",
    "10110101010101010101010101011101",
    "10000100010001000100010001000001",
    "10111111111111001111111111111101",
    "10000100010001000100010001000001",
    "10110101010101010101010101011101",
    "10100001000100010001000100000101",
    "10101111111111001111111111110101",
    "10100001000100010001000100000101",
    "10110101010101010101010101011101",
    "10000100010001000100010001000001",
    "11111111111111111111111111111111",
    "11111111111111111111111111111111",
]

# LEVEL 5: The Arena (Area tengah luas, pinggiran sempit)
LEVEL_5 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "10111111111110111111111111111101",
    "10100000000000000000000000000101",
    "10101111111110011111111111110101",
    "10101000000000000000000000010101",
    "10101011111100001111111111010101",
    "10101010000000000000000001010101",
    "10101010000000000000000001010101",
    "10101010000000000000000001010101",
    "10101010000000000000000001010101",
    "10101011111100001111111111010101",
    "10101000000000000000000000010101",
    "10101011111110011111101111110101",
    "10100000000000000000000000000101",
    "10111101111111011111111011111101",
    "10000000000000000000000000000001",
    "11111111111111111111111111111111",
]

# LEVEL 6: The Zig-Zag Plus (Zig-zag tapi ada jalan pintas vertikal)
LEVEL_6 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "11111110111111101111111110111111",
    "10000000000000000000000000000001",
    "10111111011111101111111110111101",
    "10000000000000000000000000000001",
    "11111111111111101111111111111111",
    "10000000000000000000000000000001",
    "10111100011111101111111000111101", # Potongan tengah
    "10111100011111101111111000111101",
    "10000000000000000000000000000001",
    "11111000111111101111111101111111",
    "10000000000000000000000000000001",
    "10111110011111101111100111111101",
    "10000000000000000000000000000001",
    "11100111111111101111111110011111",
    "10000000000000000000000000000001",
    "11111111111111111111111111111111",
]

# LEVEL 7: The Concentric (Kotak di dalam kotak, banyak pintu)
LEVEL_7 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "10111111100111101111111111111101",
    "10100000000000000000000000000101",
    "10101111100111101111111111110101",
    "10101000000000000000000000010101",
    "10101011100111101111111111010101",
    "10101010000000000000000001010101",
    "10101010100111101111111101010101",
    "10101010100000000000000101010101",
    "10101010100111101111111101010101",
    "10101010000000000000000001010101",
    "10101011100111101111111111010101",
    "10101000000000000000000000010101",
    "10101111110011110111111110110101",
    "10100000000000000000000000000101",
    "10111111111111101111111111111101",
    "11111111111111111111111111111111",
]

# LEVEL 8: The H-Complex (Lorong besar berbentuk H dengan banyak koneksi)
LEVEL_8 = [
    "11111111111111111111111111111111",
    "1P000000000000110000000000000001",
    "11111111111100110011111111111111",
    "10000000000000000000000000000001",
    "10111111111100110011111111111101",
    "10100000000000110000000000000101",
    "10101111111100110011111111110101",
    "10100000000000000000000000000101", # Konektor Horizontal Atas
    "10101111111100110011111000110101",
    "10101111111100110011111111110101",
    "10100000000000000000000000000101", # Konektor Horizontal Bawah
    "10101110011100110011111111110101",
    "10100000000000110000000000000101",
    "10111111111100110011111111111101",
    "10000000000000110000000000000001",
    "11111100011100110011111000011111",
    "10000000000000110000000000000001",
    "11111111111111111111111111111111",
]

# LEVEL 9: The Labyrinth (Asimetris, rumit, tapi terhubung)
LEVEL_9 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "10111111111111101111111111111101",
    "10100000000000000000000000000101",
    "10101111111111101111111111110101",
    "10100000000000101000000000000101",
    "10111111111100101001111111111101",
    "10000000000000101000000000000001",
    "11111111111100101001111111111111",
    "10000000000000000000000000000001",
    "11111111111100101001111111111111",
    "10000000000000101000000000000001",
    "10111111111100101001111111111101",
    "10100000000000101000000000000101",
    "10101111111111101111111111110101",
    "10100000000000000000000000000101",
    "10111111111111101111111111111101",
    "11111111111111111111111111111111",
]

# LEVEL 10: BOSS ARENA (Ruang terbuka lebar)
LEVEL_10 = [
    "11111111111111111111111111111111",
    "1P000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10001110000000000000000011100001",
    "10001110000000000000000011100001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10001110000000000000000011100001",
    "10001110000000000000000011100001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "10000000000000000000000000000001",
    "11111111111111111111111111111111",
]

LEVELS = [
    LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5,
    LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10
]