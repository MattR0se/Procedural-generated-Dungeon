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
        
        self.setImage()
        
        
    def setImage(self):    
        for key in self.game.room_image_dict:
            #print(self.doors, key)
            if compare(self.doors, key):
                #print('true')
                self.image = self.game.room_image_dict[key]
                return
        #self.image = self.game.room_image_dict[self.doors]
        #print('failed')
        
        
        
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
                    self.draw_text(str(j) + ', ' + str(i), 12, st.WHITE, 
                                   (pos[0] + 24, pos[1] + 12))
                    self.draw_text(str(room.doors), 12, st.WHITE, 
                                   (pos[0] + 24, pos[1] + 28))
                else:
                    pos = (margin_x + st.TILESIZE * j, margin_y + st.TILESIZE * i)
                    self.game.screen.blit(self.game.room_images[17], pos)
        
        
    def update(self):
        if self.clock.checkTime() and not self.done:
            self.build_cycle()
            #self.closeDoors()
            #self.openDoors()
            if self.done:
                print('done')
                
                '''for i in range(1, len(self.rooms)):
                    for j in range(1, len(self.rooms[i])):
                        if self.rooms[i][j]:
                            print((j, i), self.rooms[i][j].doors)'''
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
                            # pick random door constellation
                            rng = choice(st.ROOMS['N'])
                            
                            # prevent one-sided doors
                            # WORK IN PROGRESS
                            if 'N' in rng and self.rooms[i - 2][j]:
                                rng = rng.replace('N', '')
                            if 'W' in rng and self.rooms[i - 1][j - 1]:
                                rng = rng.replace('W', '')
                            if 'E' in rng and self.rooms[i - 1][j + 1]: 
                                rng = rng.replace('E', '')
  
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
                            
                            if 'N' in rng and self.rooms[i - 1][j - 1]:
                                rng = rng.replace('N', '')
                            if 'W' in rng and self.rooms[i][j - 2]: 
                                rng = rng.replace('W', '')
                            if 'S' in rng and self.rooms[i + 1][j - 1]: 
                                rng = rng.replace('S', '')
                            
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
                            
                            if 'N' in rng and self.rooms[i - 1][j + 1]:
                                rng = rng.replace('N', '')
                            if 'E' in rng and self.rooms[i][j + 2]: 
                                rng = rng.replace('E', '')
                            if 'S' in rng and self.rooms[i + 1][j + 1]: 
                                rng = rng.replace('S', '')
                            
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
                            
                            if 'W' in rng and self.rooms[i + 1][j - 1]:
                                rng = rng.replace('W', '')
                            if 'E' in rng and self.rooms[i + 1][j + 1]: 
                                rng = rng.replace('E', '')
                            if 'S' in rng and self.rooms[i + 2][j]: 
                                rng = rng.replace('S', '')
                            
                            for rm in self.room_pool:
                                if compare(rng, rm.doors):
                                    self.rooms[i + 1][j] = rm
                        self.done = False
                        return
       
        
    def closeDoors(self):
        for i in range(1, len(self.rooms) - 1):
            for j in range(1, len(self.rooms[i]) - 1):
                room = self.rooms[i][j]
                room_n = self.rooms[i - 1][j]
                room_s = self.rooms[i + 1][j]
                room_w = self.rooms[i][j - 1]
                room_e = self.rooms[i][j + 1]
                
                if room:
                    
                    for door in room.doors:  
                        
                        if door == 'N' and room_n: 
                            if 'S' not in room_n.doors:
                                print('N:', (j, i), room.doors, (j, i - 1), 
                                      room_n.doors)
                                room.doors = room.doors.replace('N', '')
                                room.setImage()
                        
                        if door == 'S' and room_s:
                            if 'N' not in room_s.doors:
                                print('S:', (j, i), room.doors, (j, i + 1), 
                                      room_s.doors)
                                room.doors = room.doors.replace('S', '')
                                room.setImage()  
                        
                        if door == 'W' and room_w:
                            if 'E' not in room_w.doors:
                                print('W:', (j, i), room.doors, (j - 1, i), 
                                      room_w.doors)
                                room.doors = room.doors.replace('W', '')
                                room.setImage()  
                                
                        if door == 'E' and room_e:
                            if 'W' not in room_e.doors:
                                print('E:', (j, i), room.doors, (j + 1, i), 
                                      room_e.doors)
                                room.doors = room.doors.replace('E', '')
                                room.setImage() 
                                
                                
    def openDoors(self):
        for i in range(1, len(self.rooms) - 1):
            for j in range(1, len(self.rooms[i]) - 1):
                room = self.rooms[i][j]
                room_n = self.rooms[i - 1][j]
                room_s = self.rooms[i + 1][j]
                room_w = self.rooms[i][j - 1]
                room_e = self.rooms[i][j + 1]
                
                if room:
                    
                    for door in room.doors:  
                        '''
                        if door == 'N' and room_n: 
                            if 'S' not in room_n.doors:
                                print('N:', (j, i), room.doors, (j, i - 1), 
                                      room_n.doors)
                                room_n.doors += 'S'
                                room_n.setImage()
                        '''
                        if door == 'S' and room_s:
                            if 'N' not in room_s.doors:
                                print('S:', (j, i), room.doors, (j, i + 1), 
                                      room_s.doors)
                                room_s.doors += 'N'
                                room_s.setImage()  
                        '''
                        if door == 'W' and room_w:
                            if 'E' not in room_w.doors:
                                print('W:', (j, i), room.doors, (j - 1, i), 
                                      room_w.doors)
                                room_w.doors += 'E'
                                room_w.setImage()  
                                
                        if door == 'E' and room_e:
                            if 'W' not in room_e.doors:
                                print('E:', (j, i), room.doors, (j + 1, i), 
                                      room_e.doors)
                                room_e.doors += 'W'
                                room_e.setImage()'''
        
        
        
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
