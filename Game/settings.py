# game settings and constants
GLOBAL_SCALE = 4
TILESIZE = 16 * GLOBAL_SCALE
TILES_W = 10
TILES_H = 8
WIDTH = TILESIZE * TILES_W
HEIGHT = TILESIZE * TILES_H
DUNGEON_SIZE = (10, 10)

FPS = 60
TITLE = 'Random generated dungeons (press R to reload)'

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
