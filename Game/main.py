import pygame as pg
import traceback
from os import path
from random import choice

import settings as st
import sprites as spr
import functions as fn
import rooms

vec = pg.math.Vector2

class Game():
    def __init__(self):
        # initialise game window etc.
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        pg.display.set_caption(st.TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        
        # boolean for room transitions (prevent player from moving if True)
        self.in_transition = False
        
        self.load_data()


    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        
        self.room_images = fn.img_list_from_strip(path.join(img_folder, 
                                                            'rooms_strip_2.png'), 
                                                  16, 16, 0, 18)
        self.room_image_dict = {
                'NSWE': self.room_images[0],
                'NS': self.room_images[1],
                'WE': self.room_images[2],
                'N': self.room_images[3],
                'S': self.room_images[4],
                'W': self.room_images[5],
                'E': self.room_images[6],
                'SW': self.room_images[7],
                'SE': self.room_images[8],
                'NE': self.room_images[9],
                'NW': self.room_images[10],
                'NWE': self.room_images[13],
                'SWE': self.room_images[14],
                'NSE': self.room_images[15],
                'NSW': self.room_images[16]
                }
        
        #self.tileset_names = ['tileset.png', 'tileset_sand.png', 
                              #'tileset_green.png','tileset_red.png']
        self.tileset_names = ['tileset.png']
        
        self.tileset_list = [fn.tileImageScale(path.join(img_folder, 
                             tileset), 16, 16, 
                             scale=1) for tileset in self.tileset_names]
        
        
    def new(self):
        # start a new game
        # initialise sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        
        # instantiate objects
        # MEMO: GET RID OF THIS ROOM NUMBER AND USE INDEX INSTEAD!
        self.dungeon = rooms.Dungeon(self, st.DUNGEON_SIZE)
        self.room_number = self.dungeon.room_map[self.dungeon.room_index[0]][
                                                 self.dungeon.room_index[1]]
        
        # pick a random tileset from all available tilesets
        self.tileset = choice(self.tileset_list)
        # create a background image from the tileset for the current room
        self.background = fn.tileRoom(self, self.tileset, self.dungeon.room_index)
        
        # spawn the player in the middle of the screen/room
        self.player = spr.Player(self, (st.WIDTH // 2 - st.TILESIZE /2, 
                                        st.HEIGHT // 2 - st.TILESIZE / 2))
        # spawn the wall objects (invisible)
        self.walls = fn.transitRoom(self, self.walls, self.dungeon, 
                                    self.room_number)
        
        self.run()


    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(st.FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        index = self.dungeon.room_index
        pg.display.set_caption(str(index) + ' ' + str(
                                self.dungeon.rooms[index[0]][index[1]].doors))
        
        # game loop update
        self.player.update(self.walls)
        #check for room transitions on screen exit (every frame)
        direction, new_room, new_pos = fn.screenWrap(self.player, 
                                                     self.dungeon)
        
        if new_room != self.room_number: 
            self.room_number = new_room
            self.RoomTransition(new_pos, direction)


    def events(self):
        # game loop events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.screen.fill((0, 0, 0))
                    self.new()


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        #self.screen.blit(self.tileset[2], (48, 48))
        #self.all_sprites.draw(self.screen)
        self.player.draw()
        #for wall in self.walls:
            #wall.draw()
        if self.dungeon.done:
            self.dungeon.blitRooms()
                
        pg.display.flip()
        
    
    def RoomTransition(self, new_pos, direction):
        # build the new room
        fn.tileRoom(self, self.tileset, self.dungeon.room_index)
        old_background = self.background
        self.background = fn.tileRoom(self, self.tileset, 
                                      self.dungeon.room_index)
        
        # scroll the new and old brackground 
        start_positions = {
                          'UP': vec(0, - st.HEIGHT),  
                          'DOWN': vec(0, st.HEIGHT),
                          'LEFT': vec(- st.WIDTH, 0),
                          'RIGHT': vec(st.WIDTH, 0)
                          }
        
        pos = start_positions[direction]
        pos2 = vec(0, 0)
       
        self.in_transition = True
        
        while pos != (0, 0):
            scroll_speed = 5
            if direction == 'UP':
                pos[1] += scroll_speed
                pos2[1] += scroll_speed
            elif direction == 'DOWN':
                pos[1] -= scroll_speed
                pos2[1] -= scroll_speed
            elif direction == 'LEFT':
                pos[0] += scroll_speed
                pos2[0] += scroll_speed
            elif direction == 'RIGHT':
                pos[0] -= scroll_speed
                pos2[0] -= scroll_speed
            
            self.screen.blit(self.background, pos)
            self.screen.blit(old_background, pos2)
            self.dungeon.blitRooms()
            self.player.draw()
            pg.display.flip()
        
        self.walls = fn.transitRoom(self, self.walls, self.dungeon, 
                                    self.room_number)
        self.player.rect.topleft = new_pos
        
        self.in_transition = False



g = Game()
try:
    while g.running:
        g.new()
except Exception:
    traceback.print_exc()
    pg.quit()

pg.quit()
