import pygame as pg
import settings as st
from random import choice
import traceback
from os import path

vec = pg.math.Vector2


def img_list_from_strip(filename, width, height, startpos, number):
    directory = path.dirname(__file__)
    file = path.join(directory, filename)
    try:
        img = pg.image.load(file).convert_alpha()
    except Exception:
        traceback.print_exc()
        return pg.Surface((width, height))
    img_set = []
    for i in range(startpos, (startpos + number)):
        rect = ((i * width, 0), (width, height))
        subimg = pg.transform.scale(img.subsurface(rect), 
                                    (st.TILESIZE, st.TILESIZE))
        img_set.append(subimg)
    return img_set


def compare(seq, string):
    # checks if string contains exactly the letters in seq, but the order 
    # is not relevant
    if len(seq) != len(string):
        return False

    for s in string:
        #print(s)
        if s not in seq:
            return False
    return True


class Room(pg.sprite.Sprite):
    def __init__(self, game, doors, type_='default'):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = type_
        #self.pos = vec(pos)
        self.doors = doors
        self.image = self.game.room_image_dict[self.doors]
        
        
        
class Dungeon(pg.sprite.Sprite):
    def __init__(self, game, size):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = vec(size)
        self.game = game
        self.font_name = pg.font.match_font(st.FONT_NAME)
          
        # for animation:
        self.clock = animationClock()    
        self.done = False
        
        # for debugging
        self.room_statistics = ''
        
        self.room_pool = [
                Room(self.game, 'NS'),  
                Room(self.game, 'WE'),  
                Room(self.game, 'N'),
                Room(self.game, 'S'),
                Room(self.game, 'W'),
                Room(self.game, 'E'),
                Room(self.game, 'WS'),
                Room(self.game, 'ES'),
                Room(self.game, 'NE'),
                Room(self.game, 'NW'),
                Room(self.game, 'NSWE'),
                Room(self.game, 'NWE'),
                Room(self.game, 'SWE'),
                Room(self.game, 'NSW'),
                Room(self.game, 'NSE')
                ]
        
        #w = st.WIDTH // st.TILESIZE
        #h = st.HEIGHT // st.TILESIZE
        w = int(self.size[0])
        h = int(self.size[1])
        # empty dungeon
        self.rooms = [[None for i in range(w)] for j in range(h)]
        # starting room
        self.rooms[h // 2][w // 2] = Room(self.game, 'NSWE', type_='start')
 
        
    
    def blitRooms(self):
        margin_x = st.TILESIZE * (st.TILES_W - self.size[0]) / 2
        margin_y = st.TILESIZE * (st.TILES_H - self.size[1]) / 2
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                room = self.rooms[i][j]
                if room:
                    pos = (margin_x + st.TILESIZE * j, margin_y + st.TILESIZE * i)
                    self.game.screen.blit(room.image, pos)
                    if room.type == 'start':
                        self.game.screen.blit(self.game.room_images[12], pos)
                    self.draw_text(str(j) + ', ' + str(i), 14, st.WHITE, 
                                   (pos[0] + 24, pos[1] + 16))
                else:
                    pos = (margin_x + st.TILESIZE * j, margin_y + st.TILESIZE * i)
                    self.game.screen.blit(self.game.room_images[17], pos)
        
        
    def update(self):
        if self.clock.checkTime() and not self.done:
            self.build_cycle()
            if self.done:
                print('done')
        self.blitRooms()    
    

    def build_cycle(self):
        self.done = True
        for i in range(1, len(self.rooms) - 1):
            for j in range(1, len(self.rooms[i]) - 1):
                room = self.rooms[i][j]
                if room:
                    if 'N' in room.doors and self.rooms[i - 1][j] == None:
                        if i == 1:
                            self.rooms[i - 1][j] = Room(self.game, 'S')
                        else:
                            rng = choice(st.ROOMS['N'])
                            for rm in self.room_pool:
                                if compare(rng, rm.doors):
                                    self.rooms[i - 1][j] = rm
                        # returns are just for animation purpose
                        self.done = False
                        return
                    
                    if 'W' in room.doors and self.rooms[i][j - 1] == None:
                        if j == 1:
                            self.rooms[i][j - 1] = Room(self.game, 'E')
                        else:
                            rng = choice(st.ROOMS['W'])
                            for rm in self.room_pool:
                                if compare(rng, rm.doors):
                                    self.rooms[i][j - 1] = rm
                        self.done = False
                        return
                    
                    if 'E' in room.doors and self.rooms[i][j + 1] == None:
                        if j == len(self.rooms) - 2:
                             self.rooms[i][j + 1] = Room(self.game, 'W')
                        else:
                            rng = choice(st.ROOMS['E'])
                            for rm in self.room_pool:
                                if compare(rng, rm.doors):
                                    self.rooms[i][j + 1] = rm
                        self.done = False                              
                        return
                    
                    if 'S' in room.doors and self.rooms[i + 1][j] == None:
                        if i == len(self.rooms) - 2:
                            pass
                            self.rooms[i + 1][j] = Room(self.game, 'N')
                        else:
                            rng = choice(st.ROOMS['S'])
                            for rm in self.room_pool:
                                if compare(rng, rm.doors):
                                    self.rooms[i + 1][j] = rm
                        self.done = False
                        return  
        
        
    def draw_text(self, text, size, color, pos):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = pos
        self.game.screen.blit(text_surface, text_rect)
        
        
        
class animationClock():
    def __init__(self):
        self.current_time = pg.time.get_ticks()
        self.wait_time = self.current_time + st.DELAY
    
    def checkTime(self):
        self.current_time = pg.time.get_ticks()
        if self.current_time >= self.wait_time:
            self.wait_time = self.current_time + st.DELAY
            return True
        return False
