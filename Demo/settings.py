# game settings and constants
TILESIZE = 48
TILES_W = 20
TILES_H = 16
WIDTH = TILESIZE * TILES_W
HEIGHT = TILESIZE * TILES_H
FPS = 60
TITLE = 'default'
FONT_NAME = 'arial'

# global setting for music and sound volume
SFX_VOL = 0.3
MU_VOL = 0.3

# game properties
DUNGEON_SIZE = (16, 16)
# animation delay in milliseconds
DELAY = 10

# possible rooms for picking
ROOMS = {
        'N': ['NS', 'NS', 'NS', 'NS', 'S', 'S', 'S', 'WS', 'ES', 'SWE', 'NSW', 'NSE'],
        'W': ['WE', 'WE', 'WE', 'WE', 'E', 'E', 'E', 'ES', 'EN', 'SWE', 'NSE', 'NWE'],
        'E': ['WE', 'WE', 'WE', 'WE', 'W', 'W', 'W', 'WS', 'WN', 'SWE', 'NSW', 'NWE'],
        'S': ['NS', 'NS', 'NS', 'NS', 'N', 'N', 'N', 'WN', 'EN', 'NSE', 'NSW', 'NWE']
        }

# default colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (0, 255, 255)
PINK = (255, 0, 255)
